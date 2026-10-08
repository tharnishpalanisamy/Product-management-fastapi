from pydantic import BaseModel , Field

class ProductCreate(BaseModel) :
    product_name : str 
    cost_price : float 
    category:str 
    quantity : int = Field(ge=1)


class ProductResponse(BaseModel) : 
    product_id :int 
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

class ProductUpdate(BaseModel) : 
    product_name : str 
    cost_price : float 
    category:str 
    quantity : int = Field(ge=1)