import asyncio
import os

from aiogram import types

from data import config
from loader import bot

loop = asyncio.get_event_loop()


async def file_uploader(file_path: str):
    sent_document = await bot.send_document(chat_id=config.DATABASE_CHANNEL, document=types.InputFile(file_path))
    os.remove(file_path)
    return sent_document["document"]["file_id"]


def get_file_id(file_path: str):
    return loop.run_until_complete(file_uploader(file_path))
