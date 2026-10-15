CREATE PROCEDURE restock_product(
    p_product_id INTEGER,
    p_quantity INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_quantity <= 0 THEN
        RAISE EXCEPTION 'Quantity must be greater than zero';
    END IF;

    UPDATE products
    SET quantity = quantity + p_quantity
    WHERE id = p_product_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product not found';
    END IF;
END;
$$;





CREATE PROCEDURE display_summary(
p_product_id INTEGER 
)
LANGUAGE plpgsql 
AS $$
DECLARE 
v_cost_price NUMERIC ; 
v_quantity INTEGER ; 
v_margin NUMERIC ; 
v_total_cost NUMERIC ;

v_selling_price NUMERIC ; 
v_estimate_sale_value NUMERIC ; 
v_profit_per_item  NUMERIC ; 
v_expected_profit NUMERIC ; 
BEGIN 
	IF NOT EXISTS (SELECT 1 FROM products WHERE id = p_product_id) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', p_product_id;
    END IF 


	SELECT p.cost_price , p.quantity , c.margin FROM products p 
	JOIN categories c on p.category_id = c.id 
	INTO v_cost_price , v_quantity , v_margin  

	SET v_selling_price := cost_price +  v_cost_price * (v_margin / 100) ; 
	SET v_total_cost := v_cost_price * v_quantity ; 
	SET v_profit_per_item := v_cost_price * (v_margin / 100) ; 
	SET v_expected_profit := v_profit_per_item * v_quantity ;  

	
	
