from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.products import PRODUCTS
from data.texts import ALL_PRODUCTS_TEXT, ASK_TRAINER_TEXT, CHOOSE_CONFIRM_TEXT
from keyboards.product import all_products_keyboard, final_cta_keyboard, product_keyboard

router = Router()


@router.callback_query(F.data.startswith("prod_more_"))
async def product_more(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_more_")
    product = PRODUCTS[key]
    features = "\n".join(product["features"])
    text = (
        f"<b>{product['title']}</b>\n"
        f"💰 {product['price']}\n\n"
        f"{product['short']}\n\n"
        f"{features}"
    )
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data.startswith("prod_why_"))
async def product_why(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_why_")
    product = PRODUCTS[key]
    text = f"<b>Почему тебе подходит «{product['title']}»</b>\n\n{product['why']}"
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data.startswith("prod_choose_"))
async def product_choose(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_choose_")
    product = PRODUCTS[key]
    text = CHOOSE_CONFIRM_TEXT.format(title=product["title"], price=product["price"])
    await callback.message.answer(text, reply_markup=final_cta_keyboard())
    await callback.answer()


@router.callback_query(F.data == "prod_other")
async def show_all_products(callback: CallbackQuery) -> None:
    await callback.message.answer(ALL_PRODUCTS_TEXT, reply_markup=all_products_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("prod_view_"))
async def product_view(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_view_")
    product = PRODUCTS[key]
    features = "\n".join(product["features"])
    text = (
        f"<b>{product['title']}</b>\n"
        f"💰 {product['price']}\n\n"
        f"{features}\n\n"
        f"<i>{product['why']}</i>"
    )
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data == "ask_trainer")
async def ask_trainer(callback: CallbackQuery) -> None:
    await callback.message.answer(ASK_TRAINER_TEXT, reply_markup=final_cta_keyboard())
    await callback.answer()