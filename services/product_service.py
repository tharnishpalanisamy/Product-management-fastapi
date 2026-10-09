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

    def _create_product_data(self, product_name:str , category:str , cost_price:float , quantity:int) -> ProductData :  
        stock_value = cost_price * quantity 
        if category not in MARGIN:
            raise InvalidCategoryException(
                f"Invalid category. Choose from: {list(MARGIN.keys())}"
            )
        margin = MARGIN[category] 
        selling_price = cost_price + (cost_price * margin / 100) 
        sales_value = selling_price * quantity
        profit_per_item = selling_price -  cost_price  
        expected_profit = profit_per_item * quantity

        product = ProductData(
            product_name=product_name,
            category=category,
            cost_price=cost_price,
            quantity=quantity,
            stock_value=stock_value,
            margin=margin,
            selling_price=selling_price,
            sale_value=sales_value,
            profit_per_item=profit_per_item,
            expected_profit=expected_profit
        )

        return product 


    async def create_product(self , product_data:ProductCreate) : 
        product = self._create_product_data(
            product_name=product_data.product_name , 
            category=product_data.category ,
            cost_price=product_data.cost_price ,
            quantity=product_data.quantity
        )

        response = await self.product_repository.create(product)
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

        product = self._create_product_data(
                    product_name=product_data.product_name , 
                    category=product_data.category ,
                    cost_price=product_data.cost_price ,
                    quantity=product_data.quantity
                )

        return await self.product_repository.update(product_id , product) 



    async def patch_product(self , product_id :int , product_data:ProductPatch) : 
        existing_product = await self.product_repository.get_by_id(id=product_id) 

        updates = product_data.model_dump(exclude_unset=True) 
 
        product_name = updates.get('product_name', existing_product['product_name']) 
        cost_price = updates.get('cost_price', existing_product['cost_price']) 
        category = updates.get('category', existing_product['category']) 
        quantity = updates.get('quantity', existing_product['quantity'])  

        product = self._create_product_data(
                product_name=product_name , 
                category=category ,
                cost_price=cost_price ,
                quantity=quantity
            ) 

        response = await self.product_repository.update(id=product_id , product = product)

        return response




