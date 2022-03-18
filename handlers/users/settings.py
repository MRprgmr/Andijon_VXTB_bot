from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from Bot.models import User
from filters.private_filters import IsAllowed
from keyboards.default.private_buttons import get_contact_send_template, get_user_settings
from loader import dp
from states.private_states import RegistrationState, SettingsState
from utils.core import get_user, send_main_menu, stoa, send_channels


@dp.message_handler(IsAllowed(), text="⚙️ Sozlamalar", state='*')
async def open_user_settings(message: types.Message, key):
    """Open user settings in main menu"""
    if key:
        user: User = await get_user(message.from_user)

        text, keyboard = await stoa(get_user_settings)(user)
        await message.answer(text=text, reply_markup=keyboard)
        await SettingsState.change_setting.set()
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(IsAllowed(), text="🖋 O'zgartirish", state=SettingsState.change_setting)
async def open_user_settings(message: types.Message, key):
    """Change user information"""
    if key:
        user: User = await get_user(message.from_user)

        text, keyboard = await stoa(get_contact_send_template)()
        await message.answer(text=text, reply_markup=keyboard)
        await RegistrationState.phone_number.set()
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(IsAllowed(), text="← Orqaga", state=SettingsState.change_setting)
async def open_user_settings(message: types.Message, state: FSMContext, key):
    """Back to main menu"""
    if key:
        user: User = await get_user(message.from_user)
        await send_main_menu(user)
        await state.finish()
    else:
        await send_channels(message.from_user.id)
