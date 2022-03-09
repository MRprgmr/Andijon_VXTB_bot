from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from django.conf import settings
from data.config import REQUIRED_CHANNELS, CHANNELS_NAMES

from Bot.models import District, User

media_root = settings.MEDIA_ROOT

# CallBack datas
district_callback = CallbackData('district_option', 'id')
school_type_callback = CallbackData('type', 'school_type')
school_name_callback = CallbackData('school_name', 'name')


def get_required_channels_checker(user):
    """Return checker message of channels that need to be joined"""
    
    text = f"Assalomu alaykum, <b>{user.first_name}</b>,\nushbu bot Andijon Xalq Ta'limi Vazirligining \nrasmiy boti bo'lib undan foydalanshi uchun \nquyidagi kannallarga a'zo bo'lish kerak 👇:"
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
                InlineKeyboardButton(text=districts[i + 1].title, callback_data=district_callback.new(id=districts[i+1].id))
            ]
        )
    if districts.count() & 1:
        keyboard_list.append(
            [
                InlineKeyboardButton(text=districts.last().title, callback_data=district_callback.new(id=districts.last.id))
            ]
        )
    keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=keyboard_list
    )

    return text, keyboard


def get_school_type():
    """Return options to choose school type"""
    
    text = "Qanday ta'lim muassasasida o'qyisiz?"
    
    keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
            InlineKeyboardButton(text="🏫 Maktab", callback_data=school_type_callback.new(school_type="public_school")),
            InlineKeyboardButton(text="🏢 Litsey", callback_data=school_type_callback.new(school_type="boarding_school"))
            ],
        ]
    )
    
    return text, keyboard

def get_schools_list(school_type: str, user: User):
    """Return list of all school in specific district"""
    
    keyboard_list = []
    district = user.district
    district: District
    if school_type == "boarding_school":
        text = "O'qiyotgan muassasangiz nomini tanlang:"
        boarding_schools = district.boarding_schools.all()
        for dist in boarding_schools:
            keyboard_list.append([InlineKeyboardButton(text=dist.title, callback_data=school_name_callback.new(name=dist.title))])
        keyboard = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=keyboard_list
        )
    else:
        text = "Maktabingiz raqamini tanlang:"
        psch = district.public_schools
        for i in range(1, psch//4+1):
            keyboard_list.append(
                [
                    InlineKeyboardButton(text=str(i*4-3), callback_data=school_name_callback.new(name=f"{i*4-3}-maktab")),
                    InlineKeyboardButton(text=str(i*4-2), callback_data=school_name_callback.new(name=f"{i*4-2}-maktab")),
                    InlineKeyboardButton(text=str(i*4-1), callback_data=school_name_callback.new(name=f"{i*4-1}-maktab")),
                    InlineKeyboardButton(text=str(i*4), callback_data=school_name_callback.new(name=f"{i*4}-maktab"))
                    
                ]
            )
        keyboard_list.append(
            [InlineKeyboardButton(text=str(i), callback_data=school_name_callback.new(name=f"{i}-maktab")) for i in range(psch-psch%3+1, psch+1)]
        )
        keyboard = InlineKeyboardMarkup(
            row_width=4,
            inline_keyboard=keyboard_list
        )
    return text, keyboard
        