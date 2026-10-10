from fastapi import FastAPI  
from routes.product_routes import router as product_router 
from routes.product_image_router import router as product_document_router
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

app.include_router(router=product_router)
app.include_router(router = product_document_router)

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

# filters = {
#     'name' : 'gift' , 
#     'cat' : 'elec'
# }

# query = '' 

# if filters :
#     conditions = [] 
#     values = [] 

#     for key in filters :
#         conditions.append(f" {key} = %s ") 
#         values.append(filters[key]) 
#     query += ' WHERE ' + ' AND ' .join(conditions) 

# print(query) 