from fastapi import APIRouter , status
from schemas.product import (
    ProductCreate , ProductUpdate , ProductPatch , ProductResponse , ProductOperationResponse
)
from services.product_service import ProductService  
from utilities.utilities import create_filters

router = APIRouter(
    prefix="/api/products", 
    tags=["product services"]
)  

product_service = ProductService() 

@router.get('/' , response_model=list[ProductResponse]) 
def get_products(
    product_name:str|None = None ,
    category:str|None = None , 
    min_quantity : int | None = None , 
    max_quantity : int | None = None , 
    min_cost:int | None = None , 
    max_cost:int | None = None 
): 


    user_filters = { 
        'product_name' : product_name , 
        'category' : category , 
        'min_quantity' : min_quantity , 
        'max_quantity' : max_quantity , 
        'min_cost' : min_cost , 
        'max_cost' : max_cost 
    } 

    filters = create_filters(user_filters)

    response = product_service.get_all_products(filters=filters)
    return response 

@router.get('/{product_id}' , response_model=ProductResponse )  
def get_product(product_id:int) :
    response = product_service.get_product_by_id(product_id)
    return response 
 

@router.post('/' , response_model=ProductOperationResponse , status_code=status.HTTP_201_CREATED) 
def create_product(product_data:ProductCreate) :  
    response = product_service.create_product(product_data)
    return response  


@router.delete('/{product_id}' , response_model=ProductOperationResponse) 
def delete_product(product_id : int ) :
    response = product_service.delete_product_by_id(product_id=product_id) 
    return response

@router.put('/{product_id}' , response_model=ProductOperationResponse) 
def update_product(product_id:int , product_data :ProductUpdate ) : 
    response = product_service.update_product(product_id=product_id , product_data=product_data)
    return response 

@router.patch('/{product_id}' , response_model=ProductOperationResponse) 
def patch_product(product_id:int , product_data:ProductPatch) :
    response = product_service.patch_product(product_id=product_id , product_data=product_data) 
    return response 