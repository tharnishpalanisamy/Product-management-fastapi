-- CREATE TABLE products(
-- product_id int generated always as identity primary key , 
-- product_name varchar(30) , 
-- category varchar(30) ,
-- cost_price numeric(10,2) , 
-- quantity int , 
-- stock_value numeric(10,2) , 
-- margin numeric(5,2) ,
-- selling_price numeric(10,2) , 
-- sale_value numeric(10,2) , 
-- profit_per_item numeric(10,2) 
-- expected_profit numeric(10,2) 
-- )


CREATE TABLE categories (
id SERIAL PRIMARY KEY , 
name VARCHAR(100) UNIQUE NOT NULL  , 
margin DECIMAL(10 , 2 ) 
)


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL CHECK (cost_price >= 0),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    category_id INTEGER NOT NULL REFERENCES categories(id)
);


CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL
);



