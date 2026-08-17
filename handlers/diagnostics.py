from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.products import PRODUCTS, build_product_card
from data.texts import (
    CATEGORY_INTRO, DIAG_INTRO,
    RECOMMENDATION_HEADER,
    Q_WORKOUTS_1, Q_WORKOUTS_2,
    Q_NUTRITION_1, Q_NUTRITION_2,
    Q_SYSTEM_1, Q_SYSTEM_2,
    Q_ONLINE_1, Q_ONLINE_2,
)
from keyboards.diagnostics import (
    workout_q1_keyboard, workout_q2_keyboard,
    nutrition_q1_keyboard, nutrition_q2_keyboard,
    system_q1_keyboard, system_q2_keyboard,
    online_q1_keyboard, online_q2_keyboard,
)
from keyboards.product import product_keyboard
from keyboards.main import main_menu_keyboard
from states import Diagnostics

router = Router()

@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    cat = callback.data
    intro = CATEGORY_INTRO.get(cat, "Хорошо, давай разберёмся 🙌")

    # ============ КНИГА (сразу) ============
    if cat == "cat_book":
        await callback.message.answer(
            f"{intro}\n\n{build_product_card('recipes')}",
            reply_markup=product_keyboard("recipes")
        )
        await callback.answer()
        return

    # ============ О ТРЕНЕРЕ (сразу) ============
    if cat == "cat_about":
        await callback.message.answer(
            "👤 <b>Валентин Михальченко</b>\n\n"
            "Вице-чемпион России, МС по фитнесу, тренер-диетолог.\n"
            "1000+ успешных кейсов.\n\n"
            "Специализация: умная трансформация тела, питание без диет, "
            "тренировки без травм.",
            reply_markup=main_menu_keyboard()
        )
        await callback.answer()
        return

    # ============ ТРЕНИРОВКИ (только 1.500₽) ============
    if cat == "cat_workouts":
        await state.set_state(Diagnostics.workout_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_WORKOUTS_1}",
            reply_markup=workout_q1_keyboard()
        )
        await callback.answer()
        return

    # ============ ПИТАНИЕ (только 5.000₽) ============
    if cat == "cat_nutrition":
        await state.set_state(Diagnostics.nutrition_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_NUTRITION_1}",
            reply_markup=nutrition_q1_keyboard()
        )
        await callback.answer()
        return

    # ============ ГОТОВАЯ СИСТЕМА (Питание+Тренировки: 11к или 23к) ============
    if cat == "cat_system":
        await state.set_state(Diagnostics.system_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_SYSTEM_1}",
            reply_markup=system_q1_keyboard()
        )
        await callback.answer()
        return

    # ============ ОНЛАЙН-ВЕДЕНИЕ (только 8.000₽) ============
    if cat == "cat_online":
        await state.set_state(Diagnostics.online_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_ONLINE_1}",
            reply_markup=online_q1_keyboard()
        )
        await callback.answer()
        return


# =================== СЦЕНАРИЙ ТРЕНИРОВОК (2 вопроса → 1.500₽) ===================
@router.callback_query(Diagnostics.workout_q1, F.data.startswith("wq1_"))
async def process_workout_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(w1=callback.data)
    await state.set_state(Diagnostics.workout_q2)
    await callback.message.answer(Q_WORKOUTS_2, reply_markup=workout_q2_keyboard())
    await callback.answer()

@router.callback_query(Diagnostics.workout_q2, F.data.startswith("wq2_"))
async def process_workout_q2(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    key = "gym_training"
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ПИТАНИЯ (2 вопроса → 5.000₽) ===================
@router.callback_query(Diagnostics.nutrition_q1, F.data.startswith("nq1_"))
async def process_nutrition_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(n1=callback.data)
    await state.set_state(Diagnostics.nutrition_q2)
    await callback.message.answer(Q_NUTRITION_2, reply_markup=nutrition_q2_keyboard())
    await callback.answer()

@router.callback_query(Diagnostics.nutrition_q2, F.data.startswith("nq2_"))
async def process_nutrition_q2(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    key = "intro"  # План питания + программа = 5.000₽
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ГОТОВОЙ СИСТЕМЫ (2 вопроса → 11к или 23к) ===================
@router.callback_query(Diagnostics.system_q1, F.data.startswith("sq1_"))
async def process_system_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(s1=callback.data)
    await state.set_state(Diagnostics.system_q2)
    await callback.message.answer(Q_SYSTEM_2, reply_markup=system_q2_keyboard())
    await callback.answer()

@router.callback_query(Diagnostics.system_q2, F.data.startswith("sq2_"))
async def process_system_q2(callback: CallbackQuery, state: FSMContext) -> None:
    budget = callback.data.removeprefix("sq2_")
    await state.clear()

    # Логика:
    # - Если готов на 23.000 → База
    # - Если до 12.000 → Комфорт
    key = "base" if budget == "high" else "comfort"
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ОНЛАЙН-ВЕДЕНИЯ (2 вопроса → 8.000₽) ===================
@router.callback_query(Diagnostics.online_q1, F.data.startswith("oq1_"))
async def process_online_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(o1=callback.data)
    await state.set_state(Diagnostics.online_q2)
    await callback.message.answer(Q_ONLINE_2, reply_markup=online_q2_keyboard())
    await callback.answer()

@router.callback_query(Diagnostics.online_q2, F.data.startswith("oq2_"))
async def process_online_q2(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    key = "online_coaching"  # 8.000₽
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}",
        reply_markup=product_keyboard(key)
    )
    await callback.answer()