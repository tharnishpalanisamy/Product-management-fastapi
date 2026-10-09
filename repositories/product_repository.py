from database.connection import get_connection 
from exceptions import DataBaseException , ProductNotFoundException 
from models import ProductData 
from database.queries import GET_QUERY , POST_QUERY , UPDATE_QUERY

class ProductRepository:
    def __init__(self) : 
        pass  

    async def create(self, product_data:ProductData   ):
        #database 
        connection = await get_connection() 
        # cursor = connection.cursor() 
        #insert 
        try :
            async with connection.cursor() as cursor:
                await cursor.execute(
                    POST_QUERY , (
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
                row = await cursor.fetchone() 

                product_id = row[0] 
                await connection.commit() 
        
                return {
                    'message': 'Product added successfully',
                    'product_id': product_id
                }
        
        except Exception as error:  
            await connection.rollback()   
            raise DataBaseException(
                f"Database operation failed: {error}"
            )
    
        finally :
            await cursor.close() 
            await connection.close()  



    async def get_all(self , filters = None ):
        connection = await get_connection() 
        

        try : 
            async with connection.cursor() as cursor :
                query = GET_QUERY 
                conditions = [] 
                values = []
                if filters :
                    
                    for key in filters : 

                        if key == 'product_name' : 
                            conditions.append(f" {key} ILIKE %s ") 
                            values.append(f"%{filters[key]}%") 
                            continue  

                        if key == 'category' : 
                            conditions.append(f" {key} = %s ") 
                            values.append(filters[key]) 
                            continue

                        if key == 'min_quantity' : 
                            conditions.append(f" quantity >= %s ") 
                            values.append(filters[key]) 
                            continue

                        if key == 'max_quantity' : 
                            conditions.append(f" quantity <= %s ") 
                            values.append(filters[key]) 
                            continue 

                        if key == 'min_cost' :
                            conditions.append(f" cost_price >= %s ") 
                            values.append(filters[key]) 
                            continue

                        if key == 'max_cost' :
                            conditions.append(f" cost_price <= %s ") 
                            values.append(filters[key]) 
                            continue 

                        
                        
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)  

                    if filters['sort_by'] == 'DESC' : 
                        query += f" ORDER BY {filters['order_by']} DESC  "
                    else : 
                        query += f" ORDER BY {filters['order_by']} "

                    query += " LIMIT %s "
                    values.append(filters["limit"]) 

                    query += " OFFSET %s "
                    values.append(filters['offset']) 


                await cursor.execute(
                    query , tuple(values) 
                )

                rows = await cursor.fetchall()  

                columns = [column[0] for column in cursor.description ] 

                products = [dict(zip(columns , row)) for row in rows ]

                return products

        except Exception as error :
             raise DataBaseException(
                f"Database operation failed: {error}"
            )

        finally :
            await connection.close() 


    async def get_by_id(self , id :int ) :
        connection = await get_connection() 

        try :
            async with connection.cursor() as cursor :
                query = GET_QUERY  + ' WHERE product_id = %s '
                await cursor.execute(
                        query, (id , )
                    )

                data = await cursor.fetchone() 

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
            await connection.close() 


    async def delete(self , id : int ) :

        product = await self.get_by_id(id) 

        if not product :
            raise ProductNotFoundException(f'Product with id {id} not found !')

        connection = await get_connection() 

        try :
            async with connection.cursor() as cursor : 

                await cursor.execute( 
                    ''' 
                    DELETE 
                    FROM products 
                    WHERE product_id = %s 
                    ''' , (id , )  
                ) 
                
                await connection.commit()  

                return { 
                    'message' : f'Product deleted successfully' ,
                    'product_id' : id 
                }  

        except Exception as error : 
            await connection.rollback() 
            raise DataBaseException(f"Database operation failed: {error}") 

        finally :
            await connection.close() 
        

    async def update(self , id : int , product  ) : 

        existing_product = await self.get_by_id(id) 

        if not existing_product :
            raise ProductNotFoundException(f'Product with id {id} not found !')

        
        connection = await get_connection() 

        try : 
            async with connection.cursor() as cursor : 
                await cursor.execute(
                    UPDATE_QUERY , (product.product_name ,
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
                
                row = await cursor.fetchone()
                product_id = row[0]
                await connection.commit() 
                return {
                    'message' : 'product updated successfully' , 
                    'product_id' : product_id
                } 
        
        except Exception as error :  
            await connection.rollback() 
            raise DataBaseException(f"Database operation failed: {error}") 

        finally :
            await connection.close()


    # def patch(self, id , product) :

    #     connection = await get_connection() 
    #     try :
    #         with connection.cursor() as cursor :  

    #             await cursor.execute(
    #                 '''
    #                 UPDATE products 
    #                 SET 
    #                     product_name = %s , 
    #                     category = %s , 
    #                     cost_price = %s ,
    #                     quantity = %s ,
    #                     stock_value = %s ,
    #                     margin = %s ,
    #                     selling_price = %s ,
    #                     sale_value = %s ,
    #                     profit_per_item = %s ,
    #                     expected_profit = %s
    #                 WHERE product_id = %s 
    #                 RETURNING product_id 
    #                 ''' , (product.product_name ,
    #                         product.category ,
    #                         product.cost_price ,
    #                         product.quantity ,
    #                         product.stock_value ,
    #                         product.margin ,
    #                         product.selling_price ,
    #                         product.sale_value ,
    #                         product.profit_per_item ,
    #                         product.expected_profit ,
    #                         id)
    #             )

    #             updated_product = await cursor.fetchone()

    #             if updated_product is None:
    #                 raise ProductNotFoundException(
    #                     f"Product with id {id} not found"
    #                 )

    #             updated_product = updated_product[0]

    #             await connection.commit() 
    #             return {
    #                 'message' : 'Product updated successfullyl' , 
    #                 'product_id' : updated_product 
    #             }

    #     except Exception as error :
    #         connection.rollback() 
    #         raise DataBaseException(f"Database operation failed: {error}")

    #     finally :
    #         await connection.close() 


