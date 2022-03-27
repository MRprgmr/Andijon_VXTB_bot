import re

from aiogram.types.message import Message
from asgiref.sync import sync_to_async

from Bot.models import User, Test
from data.config import CHANNELS
from keyboards.default.private_buttons import get_main_menu_template
from keyboards.inline.private_templates import get_required_channels_checker
from loader import dp


def stoa(x): return sync_to_async(x)


async def send_channels(user_id):
    user: User = await stoa(User.objects.get)(user_id=user_id)
    text, keyboard = await stoa(get_required_channels_checker)(user)
    await dp.bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)


async def get_user(bot_user) -> User:
    user_data = dict(user_id=bot_user.id,
                     first_name=bot_user.first_name,
                     username=bot_user.username)
    user = await stoa((await stoa(User.objects.filter)(user_id=bot_user.id)).first)()
    if not user:
        user = await stoa(User.objects.create)(**user_data)
    return user


async def phone_number_validater(message: Message) -> None:
    phone_number = message.contact.phone_number
    if phone_number[0] != '+':
        phone_number = '+' + phone_number

    if re.match(r"\+998(?:33|93|94|97|90|91|98|99|95|88)\d\d\d\d\d\d\d", phone_number) is not None:
        return phone_number
    else:
        return None


async def send_main_menu(user: User):
    text, keyboard = await stoa(get_main_menu_template)(user)
    await dp.bot.send_message(chat_id=user.user_id, text=text, reply_markup=keyboard)


async def check_all_channels(user: User):
    for i in CHANNELS:
        try:
            result = await dp.bot.get_chat_member(chat_id=int(i), user_id=user.user_id)
            if result.status in ["restricted", "left", "kicked"]:
                user.is_allowed = False
                await stoa(user.save)()
                return False
        except Exception:
            user.is_allowed = False
            await stoa(user.save)()
            return False
    user.is_allowed = True
    await stoa(user.save)()
    return True


async def get_student_result(c_a: str, s_a: str, test: Test):
    c_a = c_a.upper()
    s_a = s_a.upper()
    c = 0
    results_text = ""
    for i in range(1, len(c_a) + 1):
        if c_a[i - 1] == s_a[i - 1]:
            results_text += f"{i}.✅   "
            c += 1
        else:
            results_text += f"{i}.❌   "
        if i % 5 == 0:
            results_text += "\n—————————————————\n"
    text = f"Fan:  <b>{test.subject.title}</b>\nTest varianti raqami:  <b>{test.test_id}</b>\nTo'g'ri javoblar soni: " \
           f" <b>{c}</b> ta;\nNoto'g'ri javoblar " \
           f"soni:  <b>{len(c_a) - c}</b> ta;\n\n"
    text += results_text

    return text
