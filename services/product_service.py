from repositories.product_repository import ProductRepository 
from schemas.product import ProductCreate , ProductUpdate  , ProductPatch
from exceptions import InvalidCategoryException  , ProductNotFoundException
from database.connection import get_db 
from fastapi import Depends 
from sqlalchemy.orm import Session 


class ProductService:
    def __init__(self , db:Session) :
        self.product_repository = ProductRepository(db)  

    def create_product(self , product_data) :
        return self.product_repository.create(product_data)

    def get_all_products(self):
        return self.product_repository.get_all()  

    def get_product_by_id(self , product_id : int) :
        return self.product_repository.get_by_id(product_id)  

    def update_product(self , product_id , product_data) :
        return self.product_repository.update(product_id , product_data)

    def patch_product(self, product_id , product_data) : 
        return self.product_repository.patch(product_id , product_data)  

    def delete_product(self, product_id) :
        return self.product_repository.delete(product_id) 