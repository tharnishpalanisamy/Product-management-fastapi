from repositories.product_repository import ProductRepository 
from schemas.product import ProductCreate , ProductData 
from fastapi import HTTPException  
from exceptions import InvalidCategoryException 

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


    def create_product(self , product_data:ProductCreate) : 
        stock_value = product_data.cost_price * product_data.quantity 
        if product_data.category not in MARGIN:
            raise InvalidCategoryException(
                f"Invalid category. Choose from: {list(MARGIN.keys())}"
            )
        margin = MARGIN[product_data.category] 
        selling_price = product_data.cost_price + (product_data.cost_price * margin / 100) 
        sales_value = selling_price * product_data.quantity
        profit_per_item = selling_price -  product_data.cost_price  
        expected_profit = profit_per_item * product_data.quantity

        product = ProductData(
            product_name=product_data.product_name,
            category=product_data.category,
            cost_price=product_data.cost_price,
            quantity=product_data.quantity,
            stock_value=stock_value,
            margin=margin,
            selling_price=selling_price,
            sale_value=sales_value,
            profit_per_item=profit_per_item,
            expected_profit=expected_profit
        )

        response = self.product_repository.create(product)
        return response
        


    def get_all_products(self) :
        response = self.product_repository.get_all() 
        return response 

    def get_product_by_id(self , product_id :int ) ->dict  :
        product = self.product_repository.get_by_id(product_id) 
        return product 

    def delete_product_by_id(self,  product_id) :
        response = self.product_repository.delete(product_id) 
        return response 



