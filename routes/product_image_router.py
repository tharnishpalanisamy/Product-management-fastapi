from fastapi import APIRouter , UploadFile , File  , Depends
from database.connection import get_db
from sqlalchemy.orm import Session 
from services.product_image_service import ProductImageService

router = APIRouter(
    prefix='/productImages',
    tags = ['Product Documents']
)



@router.post('/{product_id}/images' ) 
async def create_product_image(product_id:int , file:UploadFile = File(...) , db:Session = Depends(get_db)) :
    product_image_service = ProductImageService(db)  

    return await product_image_service.upload(
        product_id=product_id , 
        file=file , 
        file_type='image'
    )


@router.post('/{product_id}/documents' ) 
async def create_product_document(product_id:int , file:UploadFile = File(...) ,db:Session = Depends(get_db) ) :
    product_image_service = ProductImageService(db) 

    return await product_image_service.upload(
            product_id=product_id , 
            file=file , 
            file_type='document'
        )

