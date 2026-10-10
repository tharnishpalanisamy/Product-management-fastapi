from fastapi import APIRouter , status , Query , File , UploadFile 
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
async def get_products(
    product_name:str|None = None ,
    category_id:int|None = None , 
    min_quantity : int | None = None , 
    max_quantity : int | None = None , 
    min_cost:int | None = None , 
    max_cost:int | None = None , 
    order_by : str = Query(default='id') , 
    limit : int = Query(default=10 , ge=1) , 
    offset:int = Query(default = 0 , ge=0) , 
    sort_by : str = 'ASC' 
    
): 


    user_filters = { 
        'product_name' : product_name , 
        'category_id' : category_id , 
        'min_quantity' : min_quantity , 
        'max_quantity' : max_quantity , 
        'min_cost' : min_cost , 
        'max_cost' : max_cost , 
        'order_by' : order_by , 
        'sort_by' : sort_by , 
        'limit' : limit , 
        'offset' : offset
    } 

    filters = create_filters(user_filters)

    response = await product_service.get_all_products(filters=filters)
    return response 

@router.get('/{product_id}' , response_model=ProductResponse )  
async def get_product(product_id:int) :
    response = await product_service.get_product_by_id(product_id)
    return response 
 

@router.post('/' , response_model=ProductOperationResponse , status_code=status.HTTP_201_CREATED) 
async def create_product(product_data:ProductCreate) :  
    response =await  product_service.create_product(product_data)
    return response  


@router.delete('/{product_id}' , response_model=ProductOperationResponse) 
async def delete_product(product_id : int ) :
    response = await product_service.delete_product_by_id(product_id=product_id) 
    return response

@router.put('/{product_id}' , response_model=ProductOperationResponse) 
async def update_product(product_id:int , product_data :ProductUpdate ) : 
    response = await product_service.update_product(product_id=product_id , product_data=product_data)
    return response 

@router.patch('/{product_id}' , response_model=ProductOperationResponse) 
async def patch_product(product_id:int , product_data:ProductPatch) :
    response = await product_service.patch_product(product_id=product_id , product_data=product_data) 
    return response 