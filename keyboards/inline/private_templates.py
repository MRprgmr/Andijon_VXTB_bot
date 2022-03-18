from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from django.conf import settings

from Bot.models import District, User
from data.config import REQUIRED_CHANNELS, CHANNELS_NAMES

media_root = settings.MEDIA_ROOT

# CallBack datas
district_callback = CallbackData('district_option', 'id')
school_name_callback = CallbackData('school_name', 'id')


def get_required_channels_checker(user):
    """Return checker message of channels that need to be joined"""

    text = f"Assalomu alaykum, <b>{user.first_name}</b>,\nushbu bot Andijon xalq ta'limi boshqarmasining \nrasmiy boti " \
           f"bo'lib, undan foydalanshi uchun \nquyidagi kannallarga a'zo bo'lish kerak 👇: "
    keyboard_list = []
    for i in range(len(REQUIRED_CHANNELS)):
        keyboard_list.append([InlineKeyboardButton(text=CHANNELS_NAMES[i], url=f"https://t.me/{REQUIRED_CHANNELS[i]}")])

    keyboard_list.append([InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_joining")])
    keyboard = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=keyboard_list
    )

    return text, keyboard


def get_all_districts():
    """Return all ditricts list from database"""

    text = "O'qiydigan tumaningizni tanlang:"
    districts = District.objects.all()
    keyboard_list = []

    if districts.count() & 1:
        end = districts.count() - 1
    else:
        end = districts.count()

    for i in range(0, end, 2):
        keyboard_list.append(
            [
                InlineKeyboardButton(text=districts[i].title, callback_data=district_callback.new(id=districts[i].id)),
                InlineKeyboardButton(text=districts[i + 1].title,
                                     callback_data=district_callback.new(id=districts[i + 1].id))
            ]
        )
    if districts.count() & 1:
        keyboard_list.append(
            [
                InlineKeyboardButton(text=districts.last().title,
                                     callback_data=district_callback.new(id=districts.last().id))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=keyboard_list
    )

    return text, keyboard


def get_schools_list(user: User):
    """Return list of all schools in specific district"""

    keyboard_list = []
    district = user.district
    district: District
    text = "O'qiyotgan muassasangiz nomini tanlang:"
    schools = district.school_set.all()
    s_c = schools.count()
    if s_c % 2 == 1:
        s_c -= 1
    for i in range(0, s_c, 2):
        keyboard_list.append(
            [
                InlineKeyboardButton(text=schools[i].title,
                                     callback_data=school_name_callback.new(id=schools[i].id)),
                InlineKeyboardButton(text=schools[i + 1].title,
                                     callback_data=school_name_callback.new(id=schools[i + 1].id))
            ]
        )
    if schools.count() % 2 == 1:
        keyboard_list.append(
            [
                InlineKeyboardButton(text=schools.last().title,
                                     callback_data=school_name_callback.new(schools.last().id))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=keyboard_list
    )
    return text, keyboard
