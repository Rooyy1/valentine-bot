from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.products import PRODUCTS, build_product_card
from data.recommend import recommend_product
from data.texts import (
    CATEGORY_INTRO,
    DIAG_INTRO,
    Q_FORMAT,
    Q_GOAL,
    Q_PROBLEM,
    RECOMMENDATION_HEADER,
)
from keyboards.diagnostics import format_keyboard, goal_keyboard, problem_keyboard
from keyboards.product import product_keyboard
from states import Diagnostics

router = Router()


@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    intro = CATEGORY_INTRO.get(callback.data, "Хорошо, давай разберёмся 🙌")
    await state.update_data(category=callback.data)

    if callback.data == "cat_book":
        text = f"{intro}\n\n{build_product_card('recipes')}"
        await callback.message.answer(text, reply_markup=product_keyboard("recipes"))
        await callback.answer()
        return

    await state.set_state(Diagnostics.goal)
    text = f"{intro}\n\n{DIAG_INTRO}\n\n{Q_GOAL}"
    await callback.message.answer(text, reply_markup=goal_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.goal, F.data.startswith("goal_"))
async def process_goal(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.removeprefix("goal_")
    await state.update_data(goal=value)
    await state.set_state(Diagnostics.problem)
    await callback.message.answer(Q_PROBLEM, reply_markup=problem_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.problem, F.data.startswith("problem_"))
async def process_problem(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.removeprefix("problem_")
    await state.update_data(problem=value)
    await state.set_state(Diagnostics.format)
    await callback.message.answer(Q_FORMAT, reply_markup=format_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.format, F.data.startswith("format_"))
async def process_format(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.removeprefix("format_")
    await state.update_data(format=value)

    data = await state.get_data()
    key, reason = recommend_product(data)
    await state.update_data(recommended=key)
    await state.set_state(None)

    product = PRODUCTS[key]
    text = _build_recommendation_text(product, reason)
    await callback.message.answer(text, reply_markup=product_keyboard(key))
    await callback.answer()


def _build_recommendation_text(product: dict, reason: str) -> str:
    features = "\n".join(product["features"])
    return (
        f"{RECOMMENDATION_HEADER}\n\n"
        f"<b>{product['title']}</b>\n"
        f"💰 {product['price']}\n\n"
        f"{features}\n\n"
        f"<i>{reason}</i>"
    )