from mailbox import Message

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.repositories.shop import product_categories, products_for_category_list

router = Router()


@router.message(Command('menu'))
async def menu(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [
        [types.InlineKeyboardButton(text='Category', callback_data='category')],
        [types.InlineKeyboardButton(text='Information for shop', callback_data='information')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return await message.answer('Press the button', reply_markup=keyboard)


@router.callback_query(F.data == 'category')
async def category(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    categories = await product_categories()
    if categories:
        buttons = []
        for category in categories:
            buttons.append([types.InlineKeyboardButton(text=category, callback_data=category)])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return await callback.message.answer('this is button - category.',
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
    await callback.message.answer(f"Категория: {callback.data}")
    products = await products_for_category_list(product_category=callback.data)
    if products:
        buttons = []
        for product in products:
            buttons.append([types.InlineKeyboardButton(text=product.product_name,
                                                       callback_data=str(product.id))])
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return await callback.message.answer('this is button - list products for select category.',
                                             reply_markup=keyboard)  # category take with your database in .env
    return await callback.message.answer('No found products in your database for select category..')