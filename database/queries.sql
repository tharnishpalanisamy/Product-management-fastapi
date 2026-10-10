
INSERT INTO categories (name , margin) VALUES 
    ('electronics' , 25 ),
    ('stationary' , 20 ),
    ('gift' , 30 ),
    ('food' , 15 ),
    ('clothes' , 30 ),
    ('wearables', 25 );


CREATE UNIQUE INDEX unique_product_file_type
ON product_images (product_id, file_type);