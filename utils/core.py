import re

from aiogram.types.message import Message
from asgiref.sync import sync_to_async

from Bot.models import User
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


async def get_student_result(c_a: str, s_a: str, test_number: int):
    results = []
    c_a = c_a.upper()
    s_a = s_a.upper()
    c = 0
    for i in range(len(c_a)):
        if c_a[i] == s_a[i]:
            results.append("✅")
            c += 1
        else:
            results.append("❌")
    text = f"Test varianti raqami:  <b>{test_number}</b>\nTo'g'ri javoblar soni:  <b>{c}</b> ta;\nNoto'g'ri javoblar " \
           f"soni:  <b>{len(c_a) - c}</b> ta;\n\n"

    text += f"  1) {s_a[0]}  {results[0]}       11) {s_a[10]}   {results[10]}       21) {s_a[20]}   {results[20]}\n" \
            f"  2) {s_a[1]}  {results[1]}       12) {s_a[11]}   {results[11]}       22) {s_a[21]}   {results[21]}\n" \
            f"  3) {s_a[2]}  {results[2]}       13) {s_a[12]}   {results[12]}       23) {s_a[22]}   {results[22]}\n" \
            f"  4) {s_a[3]}  {results[3]}       14) {s_a[13]}   {results[13]}       24) {s_a[23]}   {results[23]}\n" \
            f"  5) {s_a[4]}  {results[4]}       15) {s_a[14]}   {results[14]}       25) {s_a[24]}   {results[24]}\n" \
            f"  6) {s_a[5]}  {results[5]}       16) {s_a[15]}   {results[15]}       26) {s_a[25]}   {results[25]}\n" \
            f"  7) {s_a[6]}  {results[6]}       17) {s_a[16]}   {results[16]}       27) {s_a[26]}   {results[26]}\n" \
            f"  8) {s_a[7]}  {results[7]}       18) {s_a[17]}   {results[17]}       28) {s_a[27]}   {results[27]}\n" \
            f"  9) {s_a[8]}  {results[8]}       19) {s_a[18]}   {results[18]}       29) {s_a[28]}   {results[28]}\n" \
            f"10) {s_a[9]}  {results[9]}       20) {s_a[19]}   {results[19]}       30) {s_a[29]}   {results[29]}"

    return text
