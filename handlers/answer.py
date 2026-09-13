from mailbox import Message

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.repositories.shop import product_category_list
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
    category = await product_category_list()
    buttons = []
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return await callback.message.answer('this is button - category', reply_markup=keyboard)  # category take with your database in .env


@router.callback_query(F.data == 'information')
async def information(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    return await callback.message.answer('this is button - information')  # write information for your bot


@router.message()
async def unknow_message(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(f"I don't know this message '{message.text}', open menu - /menu")