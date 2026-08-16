from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TRAINER_USERNAME
from data.products import PRODUCTS


def product_keyboard(key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="ℹ️ Подробнее", callback_data=f"prod_more_{key}")
    builder.button(text="🤔 Почему мне это подходит", callback_data=f"prod_why_{key}")
    builder.button(text="✅ Выбрать этот вариант", callback_data=f"prod_choose_{key}")
    builder.button(text="🔄 Посмотреть другие варианты", callback_data="prod_other")
    builder.button(text="❓ Задать мне вопрос", callback_data="ask_trainer")
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


def all_products_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, product in PRODUCTS.items():
        builder.button(
            text=f"{product['title']} — {product['price']}",
            callback_data=f"prod_view_{key}",
        )
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


def final_cta_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✍️ Написать мне и оформить",
        url=f"https://t.me/{TRAINER_USERNAME}",
    )
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()