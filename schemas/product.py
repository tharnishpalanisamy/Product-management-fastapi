from pydantic import BaseModel , Field , ConfigDict

class ProductCreate(BaseModel) :
    product_name : str = Field(min_length=2 , max_length=20) 
    cost_price : float = Field(ge=1)
    quantity : int = Field(ge=1)
    category_id:int = Field(ge=1)


class ProductImageCreate(BaseModel) :
    product_id : int 
    file_path:str 
    original_filename:str 
    content_type : str 

class ProductResponse(BaseModel) : 
    model_config = ConfigDict(from_attributes=True)
    product_id :int 
    category_id:int 
    category_name : str 
    product_name : str 
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
    category_id:int = Field(ge=1)
    cost_price : float = Field(ge=1)
    quantity : int = Field(ge=1)


class ProductPatch(BaseModel) :
    product_name : str | None = Field(default=None , min_length=2 , max_length=20) 
    category_id:int | None = Field(default=None ,  ge=1)
    cost_price : float | None = Field(default=None , ge=1)  
    quantity : int | None = Field(default=None , ge=1) 


class ProductOperationResponse(BaseModel):
    message: str
    product_id: int

