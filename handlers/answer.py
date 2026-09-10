from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()

@router.message(Command('menu'))
async def menu(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [[types.InlineKeyboardButton(text='Category', callback_data='category')], [types.InlineKeyboardButton(text='Information for shop', callback_data='information')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return await message.answer( 'Press the button', reply_markup=keyboard)

@router.callback_query(F.data == 'category')
async def category(callback: CallbackQuery):
    return await callback.message.answer('this is button - category')

@router.callback_query(F.data == 'information')
async def information(callback: CallbackQuery):
    return await callback.message.answer('this is button - information')