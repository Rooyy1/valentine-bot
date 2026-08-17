from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.products import PRODUCTS, build_product_card
from data.texts import (
    ALL_PRODUCTS_TEXT,
    ASK_TRAINER_TEXT,
    CHOOSE_CONFIRM_TEXT,
    UNKNOWN_PRODUCT_TEXT,
)
from keyboards.main import main_menu_keyboard
from keyboards.product import all_products_keyboard, final_cta_keyboard, product_keyboard

router = Router()


@router.callback_query(F.data.startswith("prod_more_"))
async def product_more(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_more_")
    if key not in PRODUCTS:
        await callback.message.answer(UNKNOWN_PRODUCT_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return
    await callback.message.answer(build_product_card(key), reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data.startswith("prod_why_"))
async def product_why(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_why_")
    if key not in PRODUCTS:
        await callback.message.answer(UNKNOWN_PRODUCT_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return
    product = PRODUCTS[key]
    text = f"<b>Почему тебе подходит «{product['title']}»</b>\n\n{product['why']}"
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data.startswith("prod_choose_"))
async def product_choose(callback: CallbackQuery) -> None:
    key = callback.data.removeprefix("prod_choose_")
    if key not in PRODUCTS:
        await callback.message.answer(UNKNOWN_PRODUCT_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return
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
    # Та же карточка, что и в "Подробнее" — состав и цена продукта
    # должны выглядеть одинаково в любом месте бота.
    key = callback.data.removeprefix("prod_view_")
    if key not in PRODUCTS:
        await callback.message.answer(UNKNOWN_PRODUCT_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return
    text = f"{build_product_card(key)}\n\n<i>{PRODUCTS[key]['why']}</i>"
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


@router.callback_query(F.data == "ask_trainer")
async def ask_trainer(callback: CallbackQuery) -> None:
    await callback.message.answer(ASK_TRAINER_TEXT, reply_markup=final_cta_keyboard())
    await callback.answer()
