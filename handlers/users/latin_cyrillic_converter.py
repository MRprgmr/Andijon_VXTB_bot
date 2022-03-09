from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from Bot.models import User
from keyboards.default.private_buttons import get_back_button
from loader import dp
from filters.private_filters import IsAllowed
from states.private_states import ConverterState
from utils.core import get_user, send_main_menu, stoa
from utils.latin_krill import latin_krill_converter

latin_alphabet1 = "abdefghijklmnopqrstuvxyz"
latin_alphabet2 = "o'g'shchng"

@dp.message_handler(IsAllowed(), text="Lotin 🔄 Krill", state="*")
async def text_converter(message: types.Message):
    """Reply user when converter mode is selected"""
    
    back_button = await stoa(get_back_button)()
    
    await message.reply("🤖 Ixtiyoriy matnnni kiriting, lotindan krillga va\nkrilldan lotin xarflariga o'tkazib beraman:", reply_markup=back_button)
    await ConverterState.converter.set()
    

@dp.message_handler(IsAllowed(), text="← Orqaga", state=ConverterState.converter)
async def converter_mode(message: types.Message, state: FSMContext):
    """Back to main menu from converter mode"""
    
    user: User = await get_user(message.from_user)
    
    await state.finish()
    await send_main_menu(user)

@dp.message_handler(IsAllowed(), content_types=['text'], state=ConverterState.converter)
async def converter_mode(message: types.Message, state: FSMContext):
    """Convert given text"""
    
    text = message.text
    if text[0].lower() in latin_alphabet1 or text[:2].lower() in latin_alphabet2:
        dest = "cyrillic"
    else:
        dest = "latin"
    result = latin_krill_converter(text, dest)
    await message.reply(text=result)