from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Shop(Base):
    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    product_info: Mapped[str] = mapped_column(String(), nullable=True)
    product_category: Mapped[str] = mapped_column(String(25))
    product_price: Mapped[int] = mapped_column(BigInteger)