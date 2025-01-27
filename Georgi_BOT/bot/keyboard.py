from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_dynamic_menu(chat_enabled: bool) -> ReplyKeyboardMarkup:
    button_text = "Выключить чат" if chat_enabled else "Включить чат"
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить имя")], [KeyboardButton(text="Опции с дневником")],
            [KeyboardButton(text=button_text)],
        ],
        resize_keyboard=True
    )

def create_exercise_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Когнитивное упражнение")],
            [KeyboardButton(text="Физическое упражнение")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )

def create_completion_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выполнил")],
            [KeyboardButton(text="Не выполнил")],
        ],
        resize_keyboard=True
    )
