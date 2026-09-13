from sqlalchemy import select

from database.main import async_session
from database.models import Shop


async def product_categories():
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop.product_category).distinct(Shop.product_category)
        )

        category = filter_result.scalars().all()
    return category


async def products_for_category_list(product_category):
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop.id, Shop.product_name).filter_by(product_category=product_category)
        )

        result = filter_result.all()
    return result


async def products_list_id():
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop.id))

        products_id = filter_result.scalars().all()
    return products_id


async def product_for_id(id):
    async with async_session() as session:
        filter_result = await session.execute(
            select(Shop).filter_by(id=id))

        product = filter_result.scalar_one_or_none()
    return product
