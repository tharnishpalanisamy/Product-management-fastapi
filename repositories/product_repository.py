from database.connection import get_connection 
from exceptions import DataBaseException , ProductNotFoundException 
from models import ProductData

class ProductRepository:
    def __init__(self) : 
        pass  

    def create(self, product_data:ProductData ):
        #database 
        connection = get_connection() 
        cursor = connection.cursor() 
        #insert 
        try :
            cursor.execute(
                '''
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
                ''' , (
                    product_data.product_name , 
                    product_data.category , 
                    product_data.cost_price ,
                    product_data.quantity ,
                    product_data.stock_value ,
                    product_data.margin ,
                    product_data.selling_price ,
                    product_data.sale_value ,
                    product_data.profit_per_item ,
                    product_data.expected_profit
                    )
            )
            product_id = cursor.fetchone()[0]
            connection.commit() 
    
            return {
                'message': 'Product added successfully',
                'product_id': product_id
            }
    
        except Exception as error:  
            connection.rollback()   
            raise DataBaseException(
                f"Database operation failed: {error}"
            )
    
        finally :
            cursor.close() 
            connection.close()  



    def get_all(self):
        connection = get_connection() 
        cursor = connection.cursor() 

        try : 
            cursor.execute(
                '''
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
            )

            rows = cursor.fetchall()  

            columns = [column[0] for column in cursor.description ] 

            products = [dict(zip(columns , row)) for row in rows ]

            return products

        except Exception as error :
             raise DataBaseException(
                f"Database operation failed: {error}"
            )

        finally :
            cursor.close() 
            connection.close() 


    def get_by_id(self , id :int ) :
        connection = get_connection() 

        try :
            with connection.cursor() as cursor :
            
                cursor.execute(
                        '''
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
                        WHERE product_id = %s
                        ''' , (id , )
                    )

                data = cursor.fetchone() 

                if data is None : 
                    raise ProductNotFoundException(f'Product with id {id} not found ')


                return {
                    "product_id": data[0],
                    "product_name": data[1],
                    "category": data[2],
                    "cost_price": data[3],
                    "quantity": data[4],
                    "stock_value": data[5],
                    "margin": data[6],
                    "selling_price": data[7],
                    "sale_value": data[8],
                    "profit_per_item": data[9],
                    "expected_profit": data[10]
                } 

        except ProductNotFoundException as error :
            raise 
        except Exception as error :
            raise DataBaseException(
                    f"Database operation failed: {error}"
                )  
        
        finally :
            connection.close() 


    def delete(self , id : int ) :

        product = self.get_by_id(id) 

        if not product :
            raise ProductNotFoundException(f'Product with id {id} not found !')

        connection = get_connection() 

        try :
            with connection.cursor() as cursor : 

                cursor.execute( 
                    ''' 
                    DELETE 
                    FROM products 
                    WHERE product_id = %s 
                    ''' , (id , )  
                ) 
                
                connection.commit()  

                return {
                    'message' : f'Product with id {id} is deleted successfully'
                }  

        except Exception as error : 
            connection.rollback() 
            raise DataBaseException(f"Database operation failed: {error}") 

        finally :
            connection.close() 
        

    def update(self , id : int , product  ) : 
        connection = get_connection() 

        try : 
            with connection.cursor() as cursor : 
                cursor.execute(
                    '''
                    UPDATE products 
                    SET 
                        product_name = %s , 
                        category = %s , 
                        cost_price = %s ,
                        quantity = %s ,
                        stock_value = %s ,
                        margin = %s ,
                        selling_price = %s ,
                        sale_value = %s ,
                        profit_per_item = %s ,
                        expected_profit = %s
                    WHERE product_id = %s 
                    RETURNING product_id 
                    ''' , (product.product_name ,
                            product.category ,
                            product.cost_price ,
                            product.quantity ,
                            product.stock_value ,
                            product.margin ,
                            product.selling_price ,
                            product.sale_value ,
                            product.profit_per_item ,
                            product.expected_profit ,
                            id)
                )
                connection.commit() 
                product_id = cursor.fetchone()[0] 

                return {
                    'message' : 'product updated successfully' , 
                    'product_id' : product_id
                } 
        
        except Exception as error :  
            connection.rollback() 
            raise DataBaseException(f"Database operation failed: {error}") 

        finally :
            connection.close() 
