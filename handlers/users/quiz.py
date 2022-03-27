from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, ContentTypes

from Bot.models import User, Test
from filters.private_filters import IsAllowed, IsSubject
from keyboards.default.private_buttons import get_dtm_test_template, available_subjects_list, get_back_button
from keyboards.inline.private_templates import get_all_tests, test_book_callback, get_test_book, subject_callback
from loader import dp
from states.private_states import DTMState
from utils.core import send_channels, stoa, get_user, send_main_menu, get_student_result


@dp.message_handler(IsAllowed(), text="✅ Testlar", state="*")
async def dtm_test(message: types.Message, key):
    """Response when user press DTM Test button"""

    if key:
        text, keyboard = await stoa(get_dtm_test_template)()
        await message.answer(text=text, reply_markup=keyboard)
        await DTMState.mode_selection.set()
    else:
        await send_channels(message.from_user.id)


@dp.message_handler(text="🔙 Ortga", state=DTMState.mode_selection)
async def send_subjects_list(message: types.Message, state: FSMContext):
    """Back to main menu"""

    user: User = await get_user(message.from_user)
    await send_main_menu(user)
    await state.finish()


@dp.message_handler(text="📥 Test olish", state=DTMState.mode_selection)
async def send_subjects_list(message: types.Message):
    """Send list of available subjects"""

    text, keyboard = await stoa(available_subjects_list)()
    await message.answer(text=text, reply_markup=keyboard)
    await DTMState.subject_selection.set()


@dp.message_handler(text="🔙 Ortga", state=DTMState.subject_selection)
async def send_subjects_list(message: types.Message):
    """Back to mode selection state"""

    text, keyboard = await stoa(get_dtm_test_template)()
    await message.answer(text=text, reply_markup=keyboard)
    await DTMState.mode_selection.set()


@dp.message_handler(IsSubject(), state=DTMState.subject_selection)
async def show_available_tests(message: types.Message):
    """Show all tests in specific subject"""

    text, keyboard = await stoa(get_all_tests)(subject_title=message.text)
    msg = await message.answer("🔄", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await message.answer(text=text, reply_markup=keyboard)
    await DTMState.test_selection.set()


@dp.callback_query_handler(text="back", state=DTMState.test_selection)
async def back_to_subjects(call: CallbackQuery):
    """Back to list of subjects when back button pressed"""

    text, keyboard = await stoa(available_subjects_list)()
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=keyboard)
    await DTMState.subject_selection.set()


@dp.callback_query_handler(test_book_callback.filter(), state=DTMState.test_selection)
async def send_test_book(call: CallbackQuery, callback_data: dict):
    """Send selected test book"""

    text, keyboard, file_id = await stoa(get_test_book)(callback_data["id"])
    await call.message.delete()
    await call.message.answer_document(document=file_id, caption=text, reply_markup=keyboard)
    await DTMState.test_book_view.set()


@dp.callback_query_handler(subject_callback.filter(), state=DTMState.test_book_view)
async def back_to_subjects(call: CallbackQuery, callback_data: dict):
    """Back to list of test"""

    text, keyboard = await stoa(get_all_tests)(subject_title=callback_data["title"])
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=keyboard)
    await DTMState.test_selection.set()


@dp.message_handler(text="📝 Testni tekshirish", state=DTMState.mode_selection)
async def send_subjects_list(message: types.Message):
    """Check tests answers given by user"""

    text = "Testingiz javobini quyidagi formatda variant raqami bilan yuboring:" \
           "\n\n#123456\nabcdabcdabcdabcdabcdabcdabcdab"

    keyboard = await stoa(get_back_button)()
    await message.answer(text=text, reply_markup=keyboard)
    await DTMState.test_checker.set()


@dp.message_handler(text="← Orqaga", state=DTMState.test_checker)
async def send_subjects_list(message: types.Message):
    """Back to mode selection state"""

    text, keyboard = await stoa(get_dtm_test_template)()
    await message.answer(text=text, reply_markup=keyboard)
    await DTMState.mode_selection.set()


@dp.message_handler(content_types=ContentTypes.TEXT, state=DTMState.test_checker)
async def check_user_answers(message: types.Message):
    """Check user test answers"""

    data = message.text.split("\n")
    if len(data) != 2 or not (data[1].isalpha()) or not (data[0].startswith("#")) or not (data[0][1:].isdigit()):
        answer = "🚫 Noto'g'ri format.\nTestingiz javobini quyidagi formatda variant raqami bilan yuboring:" \
                 "\n\n#123456\nabcdabcdabcdabcdabcdabcdabcdab"
    else:
        test_id = int(data[0][1:])
        try:
            test = await stoa(Test.objects.select_related("subject").get)(test_id=test_id)
            if len(data[1]) != len(test.answers):
                answer = "🚫 Berilgan test varianti uchun javoblar soni mos emas."
            else:
                answer = await get_student_result(test.answers, data[1], test)
        except Exception as er:
            print(er)
            answer = "⚠ Kechirasiz siz bergan id raqam bo'yicha test topilmadi."

    await message.answer(text=answer)
