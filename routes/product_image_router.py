from fastapi import APIRouter , File , UploadFile 
from services.product_image_service import ProductImageService 
from typing import Annotated

router = APIRouter() 
product_image_service = ProductImageService() 


@router.post('/{product_id}/image') 
async def uplod_product_image(product_id : int , file :Annotated[UploadFile , File()] ) :
    return await product_image_service.upload(
        product_id=product_id,
        file=file,
        file_type="image",)


@router.post('/{product_id}/document') 
async def upload_product_document(product_id :int , file:Annotated[UploadFile , File()]) :
    return await product_image_service.upload(
        product_id=product_id , 
        file = file , 
        file_type = 'document'
    )

