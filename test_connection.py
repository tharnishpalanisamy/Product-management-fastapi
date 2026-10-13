
from sqlalchemy.orm import configure_mappers

from models import Category, Product, ProductImage

configure_mappers()

print("All SQLAlchemy models configured successfully!")

print(Category.__tablename__)
print(Product.__tablename__)
print(ProductImage.__tablename__)
