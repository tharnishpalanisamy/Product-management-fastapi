# app = FastAPI() 

# app.include_router(router=product_router)

# app.add_exception_handler(
#     ProductNotFoundException , 
#     product_not_found_handler
# )

# app.add_exception_handler(
#     InvalidCategoryException , 
#     invalid_category_handler
# )

# app.add_exception_handler(
#     DataBaseException , 
#     database_handler
# )


from fastapi import FastAPI
from routes.product_routes import router as product_router  
from routes.product_image_router import router as product_image_router 

app = FastAPI() 


app.include_router(product_router) 
app.include_router(product_image_router) 