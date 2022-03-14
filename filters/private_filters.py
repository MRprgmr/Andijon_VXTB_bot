from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from Bot.models import User
from data.config import ADMINS
from keyboards.inline.private_templates import get_required_channels_checker
from utils.core import get_user, stoa

class full_name_filter(BoundFilter):
    async def check(self, message: Message):

        async def is_valid(text):
            for ch in text:
                if ch.isalpha() or ch == "'":
                    continue
                else:
                    return False
            return True

        fullname = message.text.split()
        if len(fullname) == 2 and (await is_valid(fullname[0])) and (await is_valid(fullname[1])):
            return True
        else:
            await message.answer("Familiya ismingizni ketma-ket kiriting, masalan:\n\n<b>👉   Alisherov Valisher</b>")
            return False

class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        if str(message.from_user.id) in ADMINS:
            return True
        else:
            return False

class IsAllowed(BoundFilter):
    async def check(self, message: Message):
        user: User = await get_user(message.from_user)
        if not user.is_allowed:
            text, keyboard = await stoa(get_required_channels_checker)(user)
            await message.answer(text=text, reply_markup=keyboard)
            return False
        else:
            return True
        