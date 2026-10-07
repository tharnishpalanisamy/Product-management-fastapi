from fastapi import APIRouter , HTTPException
from schemas.product import ProductCreate , ProductResponse
from database.connection import get_connection  
from services.product_service import ProductService

router = APIRouter()  
product_service = ProductService() 

@router.get('/products' ) 
def get_products():
    response = product_service.get_all_products()
    return response 

@router.get('/products/{product_id}' )  
def get_product(product_id:int) :
    response = product_service.get_product_by_id(product_id)
    return response 
 

@router.post('/products' ) 
def create_product(product_data:ProductCreate) :  
    response = product_service.create_product(product_data)
    return response  


@router.delete('/products/{product_id}') 
def delete_product(product_id : int ) :
    response = product_service.delete_product_by_id(product_id=product_id) 
    return response
