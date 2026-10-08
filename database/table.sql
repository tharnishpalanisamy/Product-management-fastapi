CREATE TABLE products(
product_id int generated always as identity primary key , 
product_name varchar(30) , 
category varchar(30) ,
cost_price numeric(10,2) , 
quantity int , 
stock_value numeric(10,2) , 
margin numeric(5,2) ,
selling_price numeric(10,2) , 
sale_value numeric(10,2) , 
profit_per_item numeric(10,2) 
expected_profit numeric(10,2) 
)
