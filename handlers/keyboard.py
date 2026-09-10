from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = [[types.KeyboardButton(text='/menu')]]

    keyboard = types.ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='Press the button')
    return await message.answer('Press the button', reply_markup=keyboard)

