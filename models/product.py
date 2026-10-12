from sqlalchemy import Integer , String , Numeric 
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column 

class Base(DeclarativeBase) :
    pass 

class Product(Base) : 
    __tablename__ = 'products' 

    id : Mapped[int] = mapped_column(Integer , primary_key=True ) 
    product_name : Mapped[str] = mapped_column(String(100) , nullable=False)  
    category_id : Mapped[int] = mapped_column(Integer , nullable=False)
    cost_price : Mapped[float] = mapped_column(Numeric(10,2) , nullable=False) 
    quantity : Mapped[int] = mapped_column(Integer , nullable=False ) 