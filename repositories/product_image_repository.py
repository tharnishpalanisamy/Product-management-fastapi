
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from models.product_image import ProductImage 


class ProductImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, product_id: int,
        file_path: str, original_filename: str,
        content_type: str, file_type: str
    ) :

        statement = select(Product.id).where(
            Product.id == product_id
        )

        existing_product_id = await self.db.scalar(statement)

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
            await self.db.commit()
            await self.db.refresh(image)

            return image

        except Exception:
            await self.db.rollback()
            raise
