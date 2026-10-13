from repositories.product_repository import ProductRepository 
from schemas.product import ProductCreate , ProductUpdate  , ProductPatch
from models import ProductData
from exceptions import InvalidCategoryException  , ProductNotFoundException


class ProductService:
    def __init__(self) :
        self.product_repository = ProductRepository()  

    def create_product(self) :
        pass

    def get_all_products(self):
        pass 

    def get_product_by_id(self , product_id : int) :
        pass 

    def update_product(self) :
        pass 

    def patch_product(self) :
        pass 