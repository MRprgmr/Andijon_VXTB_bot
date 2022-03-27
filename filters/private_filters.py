from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from Bot.models import User, Subject, BookCategory
from data.config import ADMINS, CHANNELS
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
            return dict(key=False)
        else:
            return dict(key=True)


class IsMyChannel(BoundFilter):
    async def check(self, message: Message):
        if str(message.chat.id) in CHANNELS:
            return True
        else:
            return False


class IsSubject(BoundFilter):
    async def check(self, message: Message):
        try:
            subject = await stoa(Subject.objects.get)(title=message.text)
            return True
        except:
            return False


class IsBookCategory(BoundFilter):
    async def check(self, message: Message):
        try:
            category = await stoa(BookCategory.objects.get)(title=message.text)
            return True
        except:
            return False
