from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from Bot.models import User
from filters.private_filters import IsAllowed
from keyboards.default.private_buttons import get_back_button
from loader import dp
from states.private_states import ConverterState
from utils.core import get_user, send_main_menu, stoa, send_channels
from utils.latin_krill import latin_krill_converter

latin_alphabet1 = "abdefghijklmnopqrstuvxyz"
latin_alphabet2 = "o'g'shchng"


@dp.message_handler(IsAllowed(), text="Lotin 🔄 Krill", state="*")
async def text_converter(message: types.Message, key):
    """Reply user when converter mode is selected"""
    if key:
        back_button = await stoa(get_back_button)()

        await message.reply(
            "🤖 Ixtiyoriy matnnni kiriting, lotindan krillga va\nkrilldan lotin xarflariga o'tkazib beraman:",
            reply_markup=back_button)
        await ConverterState.converter.set()
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(IsAllowed(), text="← Orqaga", state=ConverterState.converter)
async def converter_mode(message: types.Message, state: FSMContext, key):
    """Back to main menu from converter mode"""
    if key:
        user: User = await get_user(message.from_user)

        await state.finish()
        await send_main_menu(user)
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(IsAllowed(), content_types=['text'], state=ConverterState.converter)
async def converter_mode(message: types.Message, state: FSMContext, key):
    """Convert given text"""
    if key:
        text = message.text
        if text[0].lower() in latin_alphabet1 or text[:2].lower() in latin_alphabet2:
            dest = "cyrillic"
        else:
            dest = "latin"
        result = latin_krill_converter(text, dest)
        await message.reply(text=result)
    else:
        await send_channels(message.from_user.id)
