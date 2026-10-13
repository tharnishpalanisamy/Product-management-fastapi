from fastapi import APIRouter , UploadFile , File 

router = APIRouter(
    prefix='/productImages'
)


@router.post('/{product_id}/images' ) 
def create_product_image(product_id:int , file:UploadFile = File(...)) :
    