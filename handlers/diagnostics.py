from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.products import PRODUCTS, build_product_card
from data.texts import (
    CATEGORY_INTRO,
    DIAG_INTRO,
    Q_WORKOUTS_1,
    Q_WORKOUTS_2,
    Q_NUTRITION_1,
    Q_NUTRITION_2,
    Q_SYSTEM_1,
    Q_SYSTEM_2,
    RECOMMENDATION_HEADER,
)
from keyboards.diagnostics import (
    workouts_goal_keyboard,
    workouts_problem_keyboard,
    nutrition_problem_keyboard,
    nutrition_goal_keyboard,
    system_frequency_keyboard,
    system_budget_keyboard,
)
from keyboards.product import product_keyboard
from states import Diagnostics
from keyboards.main import main_menu_keyboard

router = Router()


@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    cat = callback.data
    intro = CATEGORY_INTRO.get(cat, "Хорошо, давай разберёмся 🙌")

    # --- СЦЕНАРИЙ 1: КНИГА (сразу) ---
    if cat == "cat_book":
        await callback.message.answer(
            f"{intro}\n\n{build_product_card('recipes')}",
            reply_markup=product_keyboard("recipes")
        )
        await callback.answer()
        return

    # --- СЦЕНАРИЙ 2: О ТРЕНЕРЕ (сразу информация) ---
    if cat == "cat_about":
        await callback.message.answer(
            "👤 <b>Валентин Михальченко</b>\n\n"
            "Вице-чемпион России, МС по фитнесу, тренер-диетолог.\n"
            "1000+ успешных кейсов.\n\n"
            "Специализация: умная трансформация тела, питание без диет, "
            "тренировки без травм.\n\n"
            "Моя цель — помочь тебе достичь формы мечты без насилия над собой.",
            reply_markup=main_menu_keyboard()
        )
        await callback.answer()
        return

    # --- СЦЕНАРИЙ 3: ТРЕНИРОВКИ (2 вопроса) ---
    if cat == "cat_workouts":
        await state.update_data(category="workouts")
        await state.set_state(Diagnostics.workouts_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_WORKOUTS_1}",
            reply_markup=workouts_goal_keyboard()
        )
        await callback.answer()
        return

    # --- СЦЕНАРИЙ 4: ПИТАНИЕ (2 вопроса) ---
    if cat == "cat_nutrition":
        await state.update_data(category="nutrition")
        await state.set_state(Diagnostics.nutrition_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_NUTRITION_1}",
            reply_markup=nutrition_problem_keyboard()
        )
        await callback.answer()
        return

    # --- СЦЕНАРИЙ 5: ГОТОВАЯ СИСТЕМА (2 вопроса) ---
    if cat == "cat_system":
        await state.update_data(category="system")
        await state.set_state(Diagnostics.system_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_SYSTEM_1}",
            reply_markup=system_frequency_keyboard()
        )
        await callback.answer()
        return


# =========================================================
# СЦЕНАРИЙ ТРЕНИРОВКИ (2 шага)
# =========================================================
@router.callback_query(Diagnostics.workouts_q1, F.data.startswith("wgoal_"))
async def process_workouts_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(w_goal=callback.data)
    await state.set_state(Diagnostics.workouts_q2)
    await callback.message.answer(Q_WORKOUTS_2, reply_markup=workouts_problem_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.workouts_q2, F.data.startswith("wprob_"))
async def process_workouts_q2(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(w_problem=callback.data)
    await state.set_state(None)
    # ВСЕГДА выдаём персональную тренировку (1.500₽)
    key = "gym_training"
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()


# =========================================================
# СЦЕНАРИЙ ПИТАНИЯ (2 шага)
# =========================================================
@router.callback_query(Diagnostics.nutrition_q1, F.data.startswith("nprob_"))
async def process_nutrition_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(n_problem=callback.data)
    await state.set_state(Diagnostics.nutrition_q2)
    await callback.message.answer(Q_NUTRITION_2, reply_markup=nutrition_goal_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.nutrition_q2, F.data.startswith("ngoal_"))
async def process_nutrition_q2(callback: CallbackQuery, state: FSMContext) -> None:
    goal = callback.data.removeprefix("ngoal_")
    await state.update_data(n_goal=goal)
    await state.set_state(None)

    # Логика: если цель "результат" → База (23.000), иначе → Введение (5.000)
    if goal == "result":
        key = "base"
    else:
        key = "intro"

    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()


# =========================================================
# СЦЕНАРИЙ ГОТОВАЯ СИСТЕМА (2 шага)
# =========================================================
@router.callback_query(Diagnostics.system_q1, F.data.startswith("sfreq_"))
async def process_system_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(s_freq=callback.data)
    await state.set_state(Diagnostics.system_q2)
    await callback.message.answer(Q_SYSTEM_2, reply_markup=system_budget_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.system_q2, F.data.startswith("sbud_"))
async def process_system_q2(callback: CallbackQuery, state: FSMContext) -> None:
    budget = callback.data.removeprefix("sbud_")
    await state.update_data(s_budget=budget)
    await state.set_state(None)

    # Логика: бюджет "high" → База (23.000), иначе → Комфорт (11.000)
    if budget == "high":
        key = "base"
    else:
        key = "comfort"

    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()