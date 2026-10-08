from fastapi import FastAPI  
from routes.product_routes import router  
from exceptions import (
    ProductNotFoundException , 
    InvalidCategoryException , 
    DataBaseException
)

from exception_handler.exception_handler import (
    product_not_found_handler , 
    database_handler , 
    invalid_category_handler
)

app = FastAPI() 

app.include_router(router=router)

app.add_exception_handler(
    ProductNotFoundException , 
    product_not_found_handler
)

app.add_exception_handler(
    InvalidCategoryException , 
    invalid_category_handler
)

app.add_exception_handler(
    DataBaseException , 
    database_handler
)




