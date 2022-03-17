from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes

from Bot.models import User
from data.config import ADMINS
from filters.private_filters import IsAllowed
from keyboards.default.private_buttons import cancel_button
from loader import dp
from states.private_states import FeedbackState
from utils.core import get_user, send_main_menu


@dp.message_handler(IsAllowed(), text="💬 Fikr bildirish", state='*')
async def send_feedback(message: Message):
    """Ask user to enter the comment"""

    await message.answer("Bot haqida fikringiz yoki taklifingiz bo'lsa izohda qoldiring: ", reply_markup=cancel_button)
    await FeedbackState.feedback.set()


@dp.message_handler(text="🚫 Bekor qilish", state=FeedbackState.feedback)
async def cancel_feedback(message: Message, state: FSMContext):
    """Cancel sending feedback and back to main menu"""

    user: User = await get_user(message.from_user)
    await state.finish()
    await send_main_menu(user)


@dp.message_handler(content_types=ContentTypes.TEXT, state=FeedbackState.feedback)
async def send(message: Message, state: FSMContext):
    """Deliver comments to bot admins"""

    user: User = await get_user(message.from_user)
    await state.finish()
    feedback_text = "\n".join([
        f"💬 New feedback from {message.from_user.get_mention(as_html=True)}",
        f"<code>",
        message.text,
        "</code>",
    ])
    await message.answer("Izohlaringiz uchun raxmat, siz bilan tez orada aloqaga chiqishga xarakat qilamiz 😉.")
    await send_main_menu(user)
    for i in ADMINS:
        await dp.bot.send_message(i, feedback_text)
