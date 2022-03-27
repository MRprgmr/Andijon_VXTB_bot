from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Bot.models import User, Subject, BookCategory


def get_main_menu_template(lang):
    """Return main menu text and keyboard for specific language"""

    text = "Bosh menu"
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        keyboard=[
            [
                KeyboardButton(text="📚 Kitoblar")
            ],
            [
                KeyboardButton(text="Lotin 🔄 Krill"),
                KeyboardButton(text="✅ Testlar")
            ],
            [
                KeyboardButton(text="⚙️ Sozlamalar"),
                KeyboardButton(text="💬 Fikr bildirish")
            ]
        ],
        resize_keyboard=True
    )
    return text, keyboard


def get_back_button():
    back_button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="← Orqaga")]
        ],
        resize_keyboard=True
    )

    return back_button


cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚫 Bekor qilish")]
    ],
    resize_keyboard=True
)


def get_user_settings(user: User):
    """Return user settings"""

    text = f"<b>👤 Foydalanuvchi:</b>   {user.full_name}\n" \
           f"<b>📞 Telefon raqam:</b>   {user.contact}\n" \
           f"<b>📍 Tuman:</b>   {user.district.title}\n" \
           f"<b>🏫 Maktab:</b>   {user.school}"

    keyboard = ReplyKeyboardMarkup(
        row_width=1,
        keyboard=[
            [
                KeyboardButton(text="🖋 O'zgartirish"),
            ],
            [
                KeyboardButton(text="← Orqaga"),
            ]
        ],
        resize_keyboard=True,
    )

    return text, keyboard


def get_contact_send_template():
    """Return contact send text and button"""

    text = "❗️ Botdan to'liq foydalanish uchun ro'yxatdan o'tish kerak.\n\nDavom etish uchun «Raqamni jo'natish» " \
           "tugmasini bosing: "
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📲 Raqamni jo'natish",
                               request_contact=True),
            ]
        ],
        resize_keyboard=True,
    )
    return text, keyboard


def get_dtm_test_template():
    """Return template when user selected dtm test"""

    text = "Kerakli bo'limni tanlang:"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📥 Test olish"),
                KeyboardButton(text="📝 Testni tekshirish")
            ],
            [
                KeyboardButton(text="🔙 Ortga")
            ]
        ],
        resize_keyboard=True,
        row_width=2
    )
    return text, keyboard


def available_subjects_list():
    """Return list of subjects in the database"""

    text = "Testni olmoqchi bo'lgan faningizni tanlang:"
    keyboard_list = []
    subjects = Subject.objects.all()

    if subjects.count() & 1:
        end = subjects.count() - 1
    else:
        end = subjects.count()

    for i in range(0, end, 2):
        keyboard_list.append(
            [
                KeyboardButton(text=subjects[i].title),
                KeyboardButton(text=subjects[i + 1].title)
            ]
        )
    if subjects.count() & 1:
        keyboard_list.append(
            [
                KeyboardButton(text=subjects.last().title)
            ]
        )
    keyboard_list.append([KeyboardButton(text="🔙 Ortga")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_list,
        resize_keyboard=True,
        row_width=2
    )
    return text, keyboard


def get_books_categories():
    """Return set of book categories"""

    text = "Kerakli kitoblar bo'limini tanlang:"
    keyboard_list = []
    categories = BookCategory.objects.all()

    if categories.count() & 1:
        end = categories.count() - 1
    else:
        end = categories.count()

    for i in range(0, end, 2):
        keyboard_list.append(
            [
                KeyboardButton(text=categories[i].title),
                KeyboardButton(text=categories[i+1].title),
            ]
        )
    if categories.count() & 1:
        keyboard_list.append(
            [
                KeyboardButton(text=categories.last().title),
            ]
        )
    keyboard_list.append([KeyboardButton(text="🔙 Ortga")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_list,
        resize_keyboard=True,
        row_width=2
    )
    return text, keyboard
