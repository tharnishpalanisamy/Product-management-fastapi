from fastapi import FastAPI  
from routes.product_routes import router 

app = FastAPI() 

app.include_router(router=router)