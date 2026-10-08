from pydantic import BaseModel , Field

class ProductCreate(BaseModel) :
    product_name : str = Field(min_length=2 , max_length=20) 
    cost_price : float = Field(ge=1)
    category:str = Field(min_length=2 , max_length=20)
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
    product_name : str = Field(min_length=2 , max_length=20) 
    cost_price : float = Field(ge=1)
    category:str = Field(min_length=2 , max_length=20)
    quantity : int = Field(ge=1)


class ProductPatch(BaseModel) :
    product_name : str | None = Field(default=None , min_length=2 , max_length=20) 
    cost_price : float | None = Field(default=None , ge=1)  
    category : str | None = Field(default=None , min_length=2 , max_length=20) 
    quantity : int | None = Field(default=None , ge=1) 


class ProductOperationResponse(BaseModel):
    message: str
    product_id: int

