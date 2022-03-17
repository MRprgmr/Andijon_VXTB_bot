import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message, ReplyKeyboardRemove

from Bot.models import District, User, School
from filters.private_filters import IsAllowed, full_name_filter
from keyboards.default.private_buttons import get_contact_send_template
from keyboards.inline.private_templates import get_all_districts, district_callback, get_required_channels_checker, \
    get_schools_list, school_name_callback
from loader import dp
from states.private_states import RegistrationState
from utils.core import get_user, phone_number_validater, send_main_menu, check_all_channels, stoa


@dp.message_handler(IsAllowed(), CommandStart(), state='*')
async def bot_start(message: types.Message):
    """When user send command /start"""

    user: User = await get_user(message.from_user)
    is_fully_registered = await check_all_channels(user)

    if is_fully_registered:
        if not user.is_registered:
            text, keyboard = await stoa(get_contact_send_template)()
            await RegistrationState.phone_number.set()
        else:
            await send_main_menu(user)
            return
    else:
        text, keyboard = await stoa(get_required_channels_checker)(user)
    await message.answer(text=text, reply_markup=keyboard)


@dp.message_handler(IsAllowed(), state=RegistrationState.phone_number, content_types=['contact'])
async def input_phone_number(message: Message):
    """When user send contact or phone number"""

    user: User = await get_user(message.from_user)

    phone_number = await phone_number_validater(message)

    if phone_number is not None:
        user.contact = phone_number
        await stoa(user.save)()
        await message.answer(text="Familiya ismingizni ketma-ket kiriting, masalan:\n\n<b>👉   Alisherov Valisher</b>",
                             reply_markup=ReplyKeyboardRemove())
        await RegistrationState.full_name.set()
    else:
        await message.answer(text="Raqam noto'g'ri formatda jo'natildi, iltimos qayta jo'nating:")


@dp.message_handler(IsAllowed(), full_name_filter(), state=RegistrationState.full_name)
async def input_full_name(message: Message, state: FSMContext):
    """Get user full name"""

    user: User = await get_user(message.from_user)

    user.full_name = message.text
    await stoa(user.save)()

    text, keyboard = await stoa(get_all_districts)()
    await message.answer(text=text, reply_markup=keyboard)
    await RegistrationState.district_state.set()


@dp.callback_query_handler(IsAllowed(), district_callback.filter(), state=RegistrationState.district_state)
async def input_district(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """Get district name"""

    user: User = await get_user(call.from_user)
    district = await stoa(District.objects.get)(id=int(callback_data['id']))
    user.district = district
    await stoa(user.save)()

    text, keyboard = await stoa(get_schools_list)(user)
    await call.message.edit_text(text=text, reply_markup=keyboard)
    await RegistrationState.school_state.set()


@dp.callback_query_handler(IsAllowed(), school_name_callback.filter(), state=RegistrationState.school_state)
async def input_school_name(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """Get users school name"""

    user: User = await get_user(call.from_user)
    school: School = await stoa(School.objects.get)(id=int(callback_data["id"]))
    user.school = school
    user.is_registered = True
    await stoa(user.save)()
    await call.message.delete()
    await call.message.answer(
        text="🤖 Tabriklayman, siz botdan muvoffaqiyatli ro'yxatdan o'tdingiz,\n endi undan to'liq foydalana olasiz.")
    await send_main_menu(user)


@dp.callback_query_handler(text="confirm_joining", state="*")
async def check_if_user_allowed(call: types.CallbackQuery, state: FSMContext):
    """Check user when check button clicked"""

    user: User = await get_user(call.from_user)

    is_fully_registered = await check_all_channels(user)

    if is_fully_registered:
        await call.answer("✅ Tabriklayman siz endi botdan to'liq foydalan  olasiz")
        await call.message.delete()
        if not user.is_registered:
            text, keyboard = await stoa(get_contact_send_template)()
            await RegistrationState.phone_number.set()
            await call.message.answer(text=text, reply_markup=keyboard)
        else:
            await send_main_menu(user)
    else:
        await call.answer(
            "🚫 Kechirasiz botdan to'liq foydalana olmaysiz, iltimos quyidagi kanallarning barchasiga a'zo bo'lib so'ng qayta tekshiring")
