from aiogram import types

from Bot.models import User
from filters.private_filters import IsMyChannel
from keyboards.inline.private_templates import get_required_channels_checker
from loader import dp
from utils.core import get_user, stoa


@dp.chat_member_handler(IsMyChannel())
async def handler(message: types.ChatMemberUpdated):
    if message.new_chat_member.status == "left":
        user: User = await get_user(message.from_user)
        user.is_allowed = False
        await stoa(user.save)()
        text, keyboard = await stoa(get_required_channels_checker)(user)
        await dp.bot.send_message(user.user_id,
                                  text="⛔ Kechirasiz siz kannalarimizni tark etdingiz,\nbotdan to'liq foydalansih uchun"
                                       "\niltimos kanallarga qayta a'zo bo'ling!",
                                  reply_markup=keyboard
                                  )
