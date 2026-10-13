from models import Category , Product 
from sqlalchemy.orm import selectinload 
from sqlalchemy import select
from fastapi import HTTPException , status

class ProductRepository:
    def __init__(self , db) :
        self.db = db 

    def create(self , product_data) :
        statement = select(Category).where(
                Category.id == product_data.category_id
            )
        
        category = self.db.scalar(statement)
    
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
            self.db.commit() 
            self.db.refresh(product) 
    
        except Exception:
            self.db.rollback() 
    
            raise HTTPException(
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR , 
                detail = 'Unexpected Error'
            )
        return product 


    def get_all(self) :
        statement = select(Product).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        )
        products = self.db.scalars(statement=statement).all() 
    
        return products  

    def get_by_id(self, id ) :
        statement = select(Product).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        ).where(
            Product.id == id 
        )
        product = self.db.scalar(statement=statement)
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail = 'Item not found'
            )
    
        return product

    def update(self , product_id , product_data) : 
        statement = select(Product).where(
                Product.id == product_id
            )
        product = self.db.scalar(statement) 
    
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
    
            self.db.commit() 
            return {
                'message' : 'product updated successfully' , 
                'id' : product_id
            }
        except Exception :
            self.db.rollback() 
            raise 

    def patch(self, product_id , product_data) : 
        statement = select(Product).where(
                    Product.id == product_id
                )
        product = self.db.scalar(statement) 
    
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
    
            self.db.commit() 
    
            return {
                'message' : 'product updated successfully' , 
                'id' : product_id
            }
        except :
            self.db.rollback() 
            raise  

    def delete(self , id) :
        statement = select(Product).where(
            Product.id == id
        )
        product = self.db.scalar(statement) 
    
        if product is None :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , 
                detail='item not found'
            )
        try : 
            self.db.delete(product) 
            self.db.commit() 
            # self.db.refresh(product) 
    
            return {
                'message' : 'Product deleted successfully' , 
                'id' : id
            }
    
        except Exception :
            raise 