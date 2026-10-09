GET_QUERY = '''
    SELECT 
        p.id as product_id , 
        p.product_name , 
        p.category_id ,
        c.name as category_name, 
        p.cost_price , 
        p.quantity, 
        p.cost_price * p.quantity as stock_value , 
        c.margin ,
        p.cost_price * ( 1 + c.margin/100.0 )  as selling_price , 
        p.cost_price * ( 1 + c.margin/100.0 ) * p.quantity as sale_value , 
        p.cost_price * ( 1 + c.margin/100.0 ) - p.cost_price as profit_per_item ,
        ( p.cost_price * (1 + c.margin / 100.0) - p.cost_price) * p.quantity AS expected_profit

    FROM products p 
    JOIN categories c 
    ON p.category_id = c.id 
''' 


POST_QUERY = '''
    INSERT INTO products(
        product_name , 
        cost_price  , 
        quantity, 
        category_id
    ) 
    VALUES(
        %s , 
        %s , 
        %s , 
        %s 
    ) 
    RETURNING id  
'''


UPDATE_QUERY = '''
    UPDATE products 
    SET 
        product_name = %s , 
        cost_price = %s ,
        quantity = %s ,
        category_id = %s 

    WHERE id = %s 
    RETURNING id 
'''
