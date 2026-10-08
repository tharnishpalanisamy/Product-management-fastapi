from pydantic import BaseModel 

class ProductData(BaseModel): 
    product_name: str
    category: str
    cost_price: float
    quantity: int
    stock_value: float
    margin: float
    selling_price: float
    sale_value: float
    profit_per_item: float
    expected_profit: float