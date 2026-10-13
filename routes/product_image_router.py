from fastapi import APIRouter , UploadFile , File 

router = APIRouter(
    prefix='/productImages',
    tags = ['Product Documents']
)


@router.post('/{product_id}/images' ) 
def create_product_image(product_id:int , file:UploadFile = File(...)) :
    pass 


@router.post('/{product_id}/documents' ) 
def create_product_document(product_id:int , file:UploadFile = File(...)) :
    pass 


