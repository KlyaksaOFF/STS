from sqlalchemy import select

from database.main import async_session
from database.models import Shop


async def product_category_list():
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop).distinct(Shop.product_category)
        )

        category = filter_result.scalars().all()
    return category


async def products_for_category_list(product_category):
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop).filter_by(product_category=product_category)
        )

        products = filter_result.scalars().all()
    return products


async def product_for_id(id):
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop).filter_by(id=id)
        )

        product = filter_result.scalars().all()
    return product
