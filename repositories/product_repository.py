from models import Category , Product 
from sqlalchemy.orm import selectinload 
from sqlalchemy import select , text
from fastapi import HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository:
    def __init__(self , db:AsyncSession) :
        self.db = db 

    async def create(self , product_data) :
        statement = select(Category).where(
                Category.id == product_data.category_id
            )
        
        category = await self.db.scalar(statement)
    
        if category is None :
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail = 'Categoyr not found '
            )
    
        product = Product(
            product_name = product_data.product_name , 
            cost_price = product_data.cost_price ,
            quantity = product_data.quantity ,
            category = category
        )
    
        try :
            self.db.add(product)
            await self.db.commit() 
            await self.db.refresh(product) 

            stmt = select(Product).options(
                selectinload(Product.category),
                selectinload(Product.files)
            ).where(Product.id == product.id)
            
            fully_loaded_product = await self.db.scalar(stmt)
            return fully_loaded_product
    
        except Exception:
            await self.db.rollback() 
    
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR , 
                detail = 'Unexpected Error'
            )
         


    async def get_all(self,filters) :
        statement = select(Product).limit(
            filters['limit']
            ).offset(
                filters['offset']
                ).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        )
        products = (await self.db.scalars(statement=statement)).all() 
    
        return products  

    async def get_by_id(self, id ) :
        statement = select(Product).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        ).where(
            Product.id == id 
        )
        product =  await self.db.scalar(statement=statement)
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail = 'Item not found'
            )
    
        return product

    async def update(self , product_id , product_data) : 
        statement = select(Product).where(
                Product.id == product_id
            )
        product =  await self.db.scalar(statement) 
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail='item not found'
            )
    
        try :
            product.product_name = product_data.product_name 
            product.cost_price = product_data.cost_price
            product.quantity = product_data.quantity
            product.category_id = product_data.category_id 
    
            await self.db.commit() 
            return {
                'message' : 'product updated successfully' , 
                'id' : product_id
            }
        except Exception :
            await self.db.rollback() 
            raise 

    async def patch(self, product_id , product_data) : 
        statement = select(Product).where(
                    Product.id == product_id
                )
        product = await self.db.scalar(statement) 
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail='item not found'
            ) 
    
        try :
            if product_data.product_name :
                product.product_name = product_data.product_name  
            if product_data.cost_price :
                product.cost_price = product_data.cost_price
            if product_data.quantity :
                product.quantity = product_data.quantity
            if product_data.category_id :
                product.category_id = product_data.category_id 
    
            await self.db.commit() 
    
            return {
                'message' : 'product updated successfully' , 
                'id' : product_id
            }
        except :
            await self.db.rollback() 
            raise  

    async def delete(self , id) :
        statement = select(Product).where(
            Product.id == id
        )
        product = await self.db.scalar(statement) 
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail='item not found'
            )
        try : 
            await self.db.delete(product) 
            await self.db.commit() 
            # self.db.refresh(product) 
    
            return {
                'message' : 'Product deleted successfully' , 
                'id' : id
            }
    
        except Exception : 
            await self.db.rollback() 
            raise 

    async def restock(self , id, quantity) : 
        statement = text("""
                        CALL restock_product(:product_id,:quantity) 
                        """)

        try :
            await self.db.execute(statement , {'product_id' : id , 'quantity' : quantity})   
            await self.db.commit() 

            return {
                'message' : f'Quantity of product {id} is increased by {quantity}' , 
                'id' : id 
            } 
        except Exception :
            self.db.rollback() 
            raise  


    async def get_summary(self, id) :
        statement = text("""
            SELECT *
            FROM display_summary(:product_id)
        """)

        result = await self.db.execute(
            statement,
            {"product_id": id}
        )

        return result.mappings().one_or_none()