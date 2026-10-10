from pathlib import Path 
from uuid import uuid4 
from fastapi import HTTPException , UploadFile 
from repositories import ProductImageRepository 

UPLOAD_DIR = Path('upload/product') 

FILE_CONFIG = {
    'image' : {
        'types' :{
            'image/jpeg' : '.jpg' , 
            'image/png' : '.png' , 
            'image/webp' : '.webp' 
        } , 
        'max_size' : 5 * 1024 * 1024 
    }  , 
    'document' : {
        'types' : {
            'application/pdf' : '.pdf' , 
            'application/msword' : '.doc',
            'application/vnd.openxmlformats-officedocumentwordprocessingml.document' : '.docx'
        } , 
        'max_size' : 10 * 1024 * 1024 
    }
}


class ProductImageService:
    def __init__(self) :
        self.product_image_repository = ProductImageRepository() 

    async def upload(self, product_id , file:UploadFile , file_type : str ) :

        if file_type not in FILE_CONFIG :
            raise HTTPException(
                status_code=400,
                detail="File type must be image or document",
            ) 

        config = FILE_CONFIG[file_type] 

        if file.content_type not in config['types'] :
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported {file_type} format",
            )

        max_size = config['max_size']  

        contents = await file.read(max_size+1) 

        if not contents :
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty",
            ) 
        
        if len(contents) > max_size :
            raise HTTPException(
                status_code=413,
                detail=f"{file_type.title()} exceeds the size limit",
            )

        extension = config['types'][file.content_type] 
        filename = f"{uuid4().hex}{extension}" 

        UPLOAD_DIR.mkdir(parents=True , exist_ok=True ) 
        file_path = UPLOAD_DIR / filename 

        try :
            with file_path.open('wb') as destination :
                destination.write(contents) 

            result = await self.product_image_repository.create(
                product_id=product_id , 
                file_path=file_path.as_posix() , 
                original_filename=Path(file.filename or 'upload').name , 
                content_type= file.content_type , 
                file_type = file_type 
            ) 
            if result is None:
                file_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {product_id} not found",
                ) 
            return result 
        except HTTPException:
                raise

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        finally:
            await file.close()
