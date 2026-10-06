from pydantic import BaseModel 

class ProductCreate(BaseModel) :
    product_name : str 
    cost_price : float 
    category:str 
    quantity : int 


class ProductResponse(BaseModel) :
    product_name : str 
    category:str
    cost_price : float 
    quantity : int 
    stock_value : float  
    margin : float 
    selling_price : float 
    sale_value : float
    profit_per_item : float 
    expected_profit : float 

# stock_value = product_data.cost_price * product_data.quantity 
#     margin = MARGIN[product_data.category] 

#     selling_price = product_data.cost_price + (product_data.cost_price * margin / 100) 
#     profit_per_item = selling_price -  product_data.cost_price  
#     sales_value = selling_price * product_data.quantity 
#     expected_profit = profit_per_item * product_data.quantity