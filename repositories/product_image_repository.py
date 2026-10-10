from database.connection import get_connection 
from exceptions import DataBaseException 


class ProductImageRepository :
    def __init__(self) : 
        pass


    async def create(self , product_id : int , file_path :str , original_filename : str , content_type:str ,file_type: str ) :
        connection = await get_connection() 

        try :
            async with connection.cursor() as cursor :
                await cursor.execute('SELECT id FROM products WHERE id = %s ' , (product_id , ))  

                product = await cursor.fetchone() 

                if not product:
                    return None  
                
                await cursor.execute(
                    '''
                    INSERT INTO product_images (
                        product_id , 
                        file_type,
                        file_path ,  
                        original_filename , 
                        content_type    
                    )
                    VALUES (%s,%s,%s,%s , %s) 
                    RETURNING id 
                    ''' , (product_id ,file_type ,  file_path , original_filename , content_type)
                )

                row = await cursor.fetchone() 
                image_id = row[0] 
                await connection.commit() 

                return {
                    "image_id": image_id,
                    "product_id": product_id, 
                    'file_type' : file_type , 
                    "file_path": file_path,
                    "original_filename": original_filename,
                    "content_type": content_type
                }

        except Exception as error : 
            await connection.rollback() 
            raise DataBaseException(f'Error occured {error}') 
        finally:
            await connection.close() 
