from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from Bot.models import User
from filters.private_filters import IsAllowed, IsBookCategory
from keyboards.default.private_buttons import get_books_categories
from keyboards.inline.private_templates import books_in_category, book_callback, get_book, category_callback
from loader import dp
from states.private_states import LibraryState
from utils.core import send_channels, stoa, get_user, send_main_menu


@dp.message_handler(IsAllowed(), text="📚 Kitoblar", state="*")
async def dtm_test(message: types.Message, key):
    """Response when user press books button"""

    if key:
        text, keyboard = await stoa(get_books_categories)()
        await message.answer(text=text, reply_markup=keyboard)
        await LibraryState.category_selection.set()
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(text="🔙 Ortga", state=LibraryState.category_selection)
async def send_subjects_list(message: types.Message, state: FSMContext):
    """Back to main menu"""

    user: User = await get_user(message.from_user)
    await send_main_menu(user)
    await state.finish()


@dp.message_handler(IsBookCategory(), state=LibraryState.category_selection)
async def show_books_in_category(message: types.Message):
    """Show all books in specific category"""

    text, keyboard = await stoa(books_in_category)(category_title=message.text)
    msg = await message.answer("🔄", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await message.answer(text=text, reply_markup=keyboard)
    await LibraryState.book_selection.set()


@dp.callback_query_handler(text="back", state=LibraryState.book_selection)
async def back_to_subjects(call: types.CallbackQuery):
    """Back to list of categories when back button pressed"""

    text, keyboard = await stoa(get_books_categories)()
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=keyboard)
    await LibraryState.category_selection.set()


@dp.callback_query_handler(book_callback.filter(), state=LibraryState.book_selection)
async def send_test_book(call: types.CallbackQuery, callback_data: dict):
    """Send selected test book"""

    text, keyboard, file_id = await stoa(get_book)(callback_data["id"])
    await call.message.delete()
    await call.message.answer_document(document=file_id, caption=text, reply_markup=keyboard)
    await LibraryState.book_view.set()


@dp.callback_query_handler(category_callback.filter(), state=LibraryState.book_view)
async def back_to_subjects(call: types.CallbackQuery, callback_data: dict):
    """Back to list of books"""

    text, keyboard = await stoa(books_in_category)(category_title=callback_data["title"])
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=keyboard)
    await LibraryState.book_selection.set()
