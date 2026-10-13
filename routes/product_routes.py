from fastapi import APIRouter , Depends , status , HTTPException 
from sqlalchemy import Select 
from sqlalchemy.orm import Session , selectinload
from database.connection import get_db 
from models.product import Product  
from schemas.product import ProductResponse , ProductCreate , ProductUpdate , ProductPatch
from models import Category
from services.product_service import ProductService
router = APIRouter(prefix='/products' , tags = ['Products']) 


@router.get('/' , response_model=list[ProductResponse]) 
def get_products(db: Session = Depends(get_db)) : 
    product_service = ProductService(db)
    return product_service.get_all_products() 

@router.get('/{product_id}' , response_model=ProductResponse) 
def get_product(product_id:int ,db: Session = Depends(get_db) ) :
    product_service = ProductService(db)
    return product_service.get_product_by_id(product_id)

@router.post('/' , response_model=ProductResponse , status_code=status.HTTP_201_CREATED)    
def create_product(product_data :ProductCreate ,db: Session = Depends(get_db)  ) :
    product_service = ProductService(db)
    return product_service.create_product(product_data) 


@router.delete('/{product_id}') 

def delete_item(product_id:int,db: Session = Depends(get_db)) : 
    product_service = ProductService(db)
    return product_service.delete_product(product_id)


@router.put('/{product_id}') 
def update_product(product_id : int , product_data:ProductUpdate,db: Session = Depends(get_db)  )  : 
    product_service = ProductService(db)
    return product_service.update_product(product_id , product_data)

    

@router.patch('/{product_id}') 
def patch_product(product_id:int , product_data:ProductPatch,db: Session = Depends(get_db)) :
    product_service = ProductService(db)
    return product_service.patch_product(product_id , product_data)

    