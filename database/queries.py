GET_QUERY = '''
    SELECT 
        product_id , 
        product_name , 
        category , 
        cost_price , 
        quantity, 
        stock_value , 
        margin ,
        selling_price , 
        sale_value , 
        profit_per_item ,
        expected_profit 
    FROM products 
''' 


POST_QUERY = '''
    INSERT INTO products(
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
        %s 
    )
    RETURNING product_id 
'''


