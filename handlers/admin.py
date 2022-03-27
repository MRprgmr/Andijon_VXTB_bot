import asyncio
import logging

from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ContentTypes as ct
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.message import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from Bot.models import User
from filters.private_filters import IsAdmin
from loader import dp


# show admin commands --------------------------------------------
@dp.message_handler(IsAdmin(), Command('commands'), state="*")
async def show_admin_commands(message: Message):
    answer = "\n".join([
        "Admin commands:\n",
        "/broadcast — send broadcast to bot users.",
        "/send_id — send a message to user through id"
    ])
    await message.answer(answer)


# -----------------------------------------------------------------
# send message to user by admin
cancel_message = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                     keyboard=[
                                         [
                                             KeyboardButton(
                                                 text="❌ Cancel message"),
                                         ],
                                     ])


class UserMessage(StatesGroup):
    sending_confirmation = State()


@dp.message_handler(IsAdmin(), RegexpCommandsFilter(regexp_commands=["send_([0-9]*)"]), state='*')
async def send_message_to_user(message: Message, regexp_command, state: FSMContext):
    await state.update_data(user_id=regexp_command.group(1))
    await message.answer(text=f"Enter your message to be sent to the user whose id is: <code>{regexp_command.group(1)}</code>",
                         reply_markup=cancel_message)
    await UserMessage.sending_confirmation.set()


@dp.message_handler(IsAdmin(), text="❌ Cancel message", state=UserMessage.sending_confirmation)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Canceled.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsAdmin(),
                    content_types=ct.TEXT | ct.AUDIO | ct.PHOTO | ct.VIDEO | ct.VIDEO_NOTE | ct.LOCATION | ct.DOCUMENT,
                    state=UserMessage.sending_confirmation)
async def send_assigned_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data["user_id"]

    await message.send_copy(chat_id=int(user_id))
    await message.answer(f"Your message has been sent to the user <code>{user_id}</code>",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()


# -------------------------------------------------------------------
# broadcast ---------------------------------------------------------
cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,
                                    keyboard=[
                                        [
                                            KeyboardButton(
                                                text="❌ Cancel broadcast"),
                                        ],
                                    ])


class BroadCastState(StatesGroup):
    start = State()


def get_users():
    users = User.objects.all()
    result = []
    for usr in users:
        result.append(usr.user_id)
    return result


@dp.message_handler(IsAdmin(), Command('broadcast'), state="*")
async def send_broadcast(message: Message):
    await message.answer("Send a message to be broadcast:", reply_markup=cancel_button)
    await BroadCastState.start.set()


@dp.message_handler(IsAdmin(), text="❌ Cancel broadcast", state=BroadCastState.start)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Canceled.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsAdmin(),
                    content_types=ct.TEXT | ct.AUDIO | ct.PHOTO | ct.VIDEO | ct.VIDEO_NOTE | ct.LOCATION | ct.DOCUMENT,
                    state=BroadCastState.start)
async def send_broadcast_start(message: Message, state: FSMContext):
    await message.answer("Broadcast started...")
    users_ids = await sync_to_async(get_users)()
    count = 0
    try:
        for user_id in users_ids:
            try:
                await message.send_copy(user_id)
                count += 1
            except Exception as error:
                logging.info(str(error))
        await asyncio.sleep(.02)
    finally:
        await message.answer(f"Message has been sent to {count} users.", reply_markup=ReplyKeyboardRemove())
    await state.finish()
# ------------------------------------------------------------------------
