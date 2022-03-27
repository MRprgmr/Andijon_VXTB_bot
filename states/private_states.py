from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    phone_number = State()
    full_name = State()
    district_state = State()
    school_state = State()


class SettingsState(StatesGroup):
    change_setting = State()


class ConverterState(StatesGroup):
    converter = State()


class FeedbackState(StatesGroup):
    feedback = State()


class DTMState(StatesGroup):
    mode_selection = State()
    subject_selection = State()
    test_selection = State()
    test_book_view = State()
    test_checker = State()


class LibraryState(StatesGroup):
    category_selection = State()
    book_selection = State()
    book_view = State()
