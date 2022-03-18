from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from Bot.models import User


def get_main_menu_template(lang):
    """Return main menu text and keyboard for specific language"""

    text = "Bosh menu"
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        keyboard=[
            [
                KeyboardButton(text="Lotin 🔄 Krill"),
                KeyboardButton(text="📑 Yangiliklar")
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
