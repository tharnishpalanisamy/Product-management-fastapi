from fastapi import APIRouter 
from schemas.product import ProductCreate 
from database.connection import get_connection 
router = APIRouter() 

MARGIN = {
    'electronics' : 25 , 
    'stationary' : 20 , 
    'gift' : 24 , 
    'food' : 20 , 
    'clothes' : 35 , 
    'wearables' : 30
}

@router.get('/products') 
def get_all_products():
    return {
        'message' : 'All products'
    }

@router.get('/products/{product_id}'  )  
def get_product_by_id(product_id:int) :
    return {
        'Message' : 'product by id ' ,
        'id' : product_id 
    }




@router.post('/products' ) 
def add_product(product_data:ProductCreate) :  

    #data calculations 
    stock_value = product_data.cost_price * product_data.quantity 
    margin = MARGIN[product_data.category] 
    selling_price = product_data.cost_price + (product_data.cost_price * margin / 100) 
    sales_value = selling_price * product_data.quantity
    profit_per_item = selling_price -  product_data.cost_price  
    expected_profit = profit_per_item * product_data.quantity

    #database 
    connection = get_connection() 
    cursor = connection.cursor() 

    #insert 
    cursor.execute(
        '''
        INSERT INTO products(
            product_name , 
            category , 
            product_id  , 
            product_name , 
            category ,
            cost_price  , 
            quantity, 
            stock_value , 
            margin ,
            selling_price , 
            sale_value , 
            profit_per_item ,
            expected_profit 
        ) 
        VALUES(
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s , 
            %s 
        )
        RETURNING product_id 
        ''' , (product_data.product_name)
    )


# product_name : str 
#     category:str
#     cost_price : float 
#     quantity : int 
#     stock_value : float  
#     margin : float 
#     selling_price : float 
#     sale_value : float
#     profit_per_item : float 
#     expected_profit : float 