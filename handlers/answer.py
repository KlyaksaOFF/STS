from mailbox import Message

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.repositories.shop import product_categories, product_for_id, products_for_category_list, products_list_id

router = Router()


@router.message(Command('menu'))
async def menu(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [
        [types.InlineKeyboardButton(text='Categories', callback_data='categories')],
        [types.InlineKeyboardButton(text='Information for shop', callback_data='information')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return await message.answer('Press the button', reply_markup=keyboard)


@router.callback_query(F.data == 'categories')
async def category(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    categories = await product_categories()
    if categories:
        buttons = []
        for category in categories:
            buttons.append([types.InlineKeyboardButton(text=category, callback_data=category)])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return await callback.message.answer('Categories:',
                                             reply_markup=keyboard)  # category take with your database in .env
    return await callback.message.answer('No found categories in your database.')


@router.callback_query(F.data == 'information')
async def information(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    return await callback.message.answer('this is button - information')  # write information for your bot


@router.message()
async def unknow_message(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(f"I don't know this message '{message.text}', open menu - /menu")


async def is_category(callback: types.CallbackQuery) -> bool:
    categories = await product_categories()
    return callback.data in categories


@router.callback_query(is_category)
async def handle_category(callback: types.CallbackQuery):
    products = await products_for_category_list(product_category=callback.data)
    if products:
        buttons = []
        for product in products:
            buttons.append([types.InlineKeyboardButton(text=product.product_name,
                                                       callback_data=str(product.id))])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return await callback.message.answer(f"Category: {callback.data}",
                                             reply_markup=keyboard)  # category take with your database in .env
    return await callback.message.answer('No found products in your database for select category..')


async def is_product(callback: types.CallbackQuery) -> bool:
    if not callback.data.isdigit():
        return False
    products = await products_list_id()
    return int(callback.data) in products


@router.callback_query(is_product)
async def handle_product(callback: types.CallbackQuery):
    product = await product_for_id(id=int(callback.data))
    if product:
        buttons = [[types.InlineKeyboardButton(text='Buy this product',
                                                callback_data=f'buy_product{product.id}')]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return await callback.message.answer(f"Id product: {product.id} \n"
                                      f"Category: {product.product_category} \n"
                                      f"Name: {product.product_name} \n"
                                      f"Information: {product.product_info} \n"
                                      f"Price: {product.product_price}",
                                      reply_markup=keyboard)  # product take with your database in .env
    return await callback.message.answer('No found this product in your database.')


@router.callback_query(F.data.startswith('buy_product'))
async def buy_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('BUYYY')