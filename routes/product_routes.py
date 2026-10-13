# from fastapi import APIRouter , status , Query
# from schemas.product import (
#     ProductCreate , ProductUpdate , ProductPatch , ProductResponse , ProductOperationResponse
# )
# from services.product_service import ProductService  
# from utilities.utilities import create_filters

# router = APIRouter(
#     prefix="/api/products", 
#     tags=["product services"]
# )  

# product_service = ProductService() 

# @router.get('/' , response_model=list[ProductResponse]) 
# async def get_products(
#     product_name:str|None = None ,
#     category:str|None = None , 
#     min_quantity : int | None = None , 
#     max_quantity : int | None = None , 
#     min_cost:int | None = None , 
#     max_cost:int | None = None , 
#     order_by : str = Query(default='product_id') , 
#     limit : int = Query(default=10 , ge=1) , 
#     offset:int = Query(default = 0 , ge=0) , 
#     sort_by : str = 'ASC' 
    
# ): 


#     user_filters = { 
#         'product_name' : product_name , 
#         'category' : category , 
#         'min_quantity' : min_quantity , 
#         'max_quantity' : max_quantity , 
#         'min_cost' : min_cost , 
#         'max_cost' : max_cost , 
#         'order_by' : order_by , 
#         'sort_by' : sort_by , 
#         'limit' : limit , 
#         'offset' : offset
#     } 

#     filters = create_filters(user_filters)

#     response = await product_service.get_all_products(filters=filters)
#     return response 

# @router.get('/{product_id}' , response_model=ProductResponse )  
# async def get_product(product_id:int) :
#     response = await product_service.get_product_by_id(product_id)
#     return response 
 

# @router.post('/' , response_model=ProductOperationResponse , status_code=status.HTTP_201_CREATED) 
# async def create_product(product_data:ProductCreate) :  
#     response =await  product_service.create_product(product_data)
#     return response  


# @router.delete('/{product_id}' , response_model=ProductOperationResponse) 
# async def delete_product(product_id : int ) :
#     response = await product_service.delete_product_by_id(product_id=product_id) 
#     return response

# @router.put('/{product_id}' , response_model=ProductOperationResponse) 
# async def update_product(product_id:int , product_data :ProductUpdate ) : 
#     response = await product_service.update_product(product_id=product_id , product_data=product_data)
#     return response 

# @router.patch('/{product_id}' , response_model=ProductOperationResponse) 
# async def patch_product(product_id:int , product_data:ProductPatch) :
#     response = await product_service.patch_product(product_id=product_id , product_data=product_data) 
#     return response 



from fastapi import APIRouter , Depends , status , HTTPException 
from sqlalchemy import select 
from sqlalchemy.orm import Session , selectinload
from database.connection import get_db 
from models.product import Product  
from schemas.product import ProductResponse , ProductCreate 
from models import Category

router = APIRouter(prefix='/products' , tags = ['Products']) 

@router.get('/' , response_model=list[ProductResponse]) 
def get_products(db : Session = Depends(get_db)) :
    statement = select(Product).options(
        selectinload(Product.category)
    )
    products = db.scalars(statement=statement).all() 

    return products 

@router.get('/{product_id}' , response_model=ProductResponse) 
def get_product(product_id:int , db : Session = Depends(get_db)) :
    statement = select(Product).options(
        selectinload(Product.category)
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