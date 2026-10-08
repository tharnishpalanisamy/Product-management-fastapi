from fastapi import APIRouter 
from schemas.product import ProductCreate , ProductUpdate , ProductPatch
from database.connection import get_connection  
from services.product_service import ProductService

router = APIRouter(
    prefix="/api/products", 
    tags=["product services"]
)  

product_service = ProductService() 

@router.get('' ) 
def get_products():
    response = product_service.get_all_products()
    return response 

@router.get('/{product_id}' )  
def get_product(product_id:int) :
    response = product_service.get_product_by_id(product_id)
    return response 
 

@router.post('') 
def create_product(product_data:ProductCreate) :  
    response = product_service.create_product(product_data)
    return response  


@router.delete('/{product_id}') 
def delete_product(product_id : int ) :
    response = product_service.delete_product_by_id(product_id=product_id) 
    return response

@router.put('/{product_id}') 
def update_product(product_id:int , product_data :ProductUpdate ) : 
    response = product_service.update_product(product_id=product_id , product_data=product_data)
    return response 

@router.patch('/{product_id}') 
def patch_product(product_id:int , product_data:ProductPatch) :
    response = product_service.patch_product(product_id=product_id , product_data=product_data) 
    return response 