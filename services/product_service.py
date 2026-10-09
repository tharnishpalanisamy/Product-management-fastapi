from repositories.product_repository import ProductRepository 
from schemas.product import ProductCreate , ProductUpdate  , ProductPatch
from models import ProductData
from exceptions import InvalidCategoryException  , ProductNotFoundException

MARGIN = {
    'electronics' : 25 , 
    'stationary' : 20 , 
    'gift' : 24 , 
    'food' : 20 , 
    'clothes' : 35 , 
    'wearables' : 30
}

class ProductService:
    def __init__(self) :
        self.product_repository = ProductRepository()  

    async def create_product(self , product_data:ProductCreate) : 

        response = await self.product_repository.create(product_data) 
        return response
        


    async def get_all_products(self , filters = None ) :
        response = await self.product_repository.get_all(filters = filters) 
        return response 

    async def get_product_by_id(self , product_id :int ) ->dict  :
        product = await self.product_repository.get_by_id(product_id) 
        return product 

    async def delete_product_by_id(self,  product_id) :
        response = await self.product_repository.delete(product_id) 
        return response 

    async def update_product(self , product_id : int , product_data :ProductUpdate  ) : 

        return await self.product_repository.update(product_id , product_data) 



    async def patch_product(self , product_id :int , product_data:ProductPatch) : 
        existing_product = await self.product_repository.get_by_id(id=product_id) 

        updates = product_data.model_dump(exclude_unset=True) 
 
        product_name = updates.get('product_name', existing_product['product_name']) 
        cost_price = updates.get('cost_price', existing_product['cost_price']) 
        category_id = updates.get('category', existing_product['category_id']) 
        quantity = updates.get('quantity', existing_product['quantity'])  

        product_data.product_name = product_name  
        product_data.cost_price = cost_price
        product_data.category_id = category_id
        product_data.quantity = quantity

        response = await self.product_repository.update(id=product_id , product = product_data)

        return response




