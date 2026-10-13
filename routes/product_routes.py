from fastapi import APIRouter , Depends , status , HTTPException 
from sqlalchemy import select 
from sqlalchemy.orm import Session , selectinload
from database.connection import get_db 
from models.product import Product  
from schemas.product import ProductResponse , ProductCreate , ProductUpdate , ProductPatch
from models import Category

router = APIRouter(prefix='/products' , tags = ['Products']) 

@router.get('/' , response_model=list[ProductResponse]) 
def get_products(db : Session = Depends(get_db)) :
    statement = select(Product).options(
        selectinload(Product.category) , 
        selectinload(Product.files)
    )
    products = db.scalars(statement=statement).all() 

    return products 

@router.get('/{product_id}' , response_model=ProductResponse) 
def get_product(product_id:int , db : Session = Depends(get_db)) :
    statement = select(Product).options(
        selectinload(Product.category) , 
        selectinload(Product.files)
    ).where(
        Product.id == product_id 
    )
    product = db.scalar(statement=statement)

    if product is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail = 'Item not found'
        )

    return product 

@router.post('/' , response_model=ProductResponse , status_code=status.HTTP_201_CREATED)    
def create_product(product_data :ProductCreate , db : Session = Depends(get_db) ) :
    statement = select(Category).where(
        Category.id == product_data.category_id
    )

    category = db.scalar(statement)

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
        db.add(product)
        db.commit() 
        db.refresh(product) 

    except Exception:
        db.rollback() 

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR , 
            detail = 'Unexpected Error'
        )
    return product  


@router.delete('/{product_id}') 

def delete_item(product_id:int , session:Session = Depends(get_db)) : 
    statement = select(Product).where(
        Product.id == product_id
    )
    product = session.scalar(statement) 

    if product is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , 
            detail='item not found'
        )
    try : 
        session.delete(product) 
        session.commit() 
        # session.refresh(product) 

        return {
            'message' : 'Product deleted successfully' , 
            'id' : product_id
        }

    except Exception :
        raise 


@router.put('/{product_id}') 
def update_product(product_id : int , product_data:ProductUpdate  ,  session:Session = Depends(get_db))  : 
    statement = select(Product).where(
            Product.id == product_id
        )
    product = session.scalar(statement) 

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

        session.commit() 
        return {
            'message' : 'product updated successfully' , 
            'id' : product_id
        }
    except Exception :
        session.rollback() 
        raise 

    

@router.patch('/{product_id}') 
def patch_product(product_id:int , product_data:ProductPatch , session:Session = Depends(get_db)) :

    statement = select(Product).where(
                Product.id == product_id
            )
    product = session.scalar(statement) 

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

        session.commit() 

        return {
            'message' : 'product updated successfully' , 
            'id' : product_id
        }
    except :
        session.rollback() 
        raise 