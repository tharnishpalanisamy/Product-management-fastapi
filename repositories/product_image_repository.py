
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.product import Product
from models.product_image import ProductImage


class ProductImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, product_id: int,
        file_path: str, original_filename: str,
        content_type: str, file_type: str
    ) :

        statement = select(Product.id).where(
            Product.id == product_id
        )

        existing_product_id = self.db.scalar(statement)

        if existing_product_id is None:
            return None

        image = ProductImage(
            product_id=product_id,
            file_path=file_path,
            original_filename=original_filename,
            content_type=content_type,
            file_type=file_type,
        )

        try:
            self.db.add(image)
            self.db.commit()
            self.db.refresh(image)

            return image

        except Exception:
            self.db.rollback()
            raise
