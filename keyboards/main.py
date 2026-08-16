from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏋️ Хочу разобраться с тренировками", callback_data="cat_workouts")
    builder.button(text="🥗 Хочу наладить питание", callback_data="cat_nutrition")
    builder.button(text="🎯 Хочу готовую систему", callback_data="cat_system")
    builder.button(text="📖 Хочу купить книгу рецептов", callback_data="cat_book")
    builder.button(text="👤 Хочу узнать о тренере", callback_data="cat_about")
    builder.adjust(1)
    return builder.as_markup()
