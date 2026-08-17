from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data.products import build_product_card
from data.recommend import (
    recommend_nutrition,
    recommend_online,
    recommend_system,
    recommend_workout,
)
from data.texts import (
    ABOUT_TRAINER_TEXT,
    CATEGORY_INTRO,
    DIAG_INTRO,
    DIAG_INTRO_SHORT,
    Q_NUTRITION_1,
    Q_NUTRITION_2,
    Q_ONLINE_1,
    Q_ONLINE_2,
    Q_SYSTEM_1,
    Q_WORKOUTS_1,
    Q_WORKOUTS_2,
    RECOMMENDATION_HEADER,
)
from keyboards.diagnostics import (
    nutrition_q1_keyboard,
    nutrition_q2_keyboard,
    online_q1_keyboard,
    online_q2_keyboard,
    system_q1_keyboard,
    workout_q1_keyboard,
    workout_q2_keyboard,
)
from keyboards.main import main_menu_keyboard
from keyboards.product import product_keyboard
from states import Diagnostics

router = Router()


@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    cat = callback.data
    intro = CATEGORY_INTRO.get(cat, "Хорошо, давай разберёмся 🙌")
    # На случай, если пользователь заходит в новую категорию посреди старого сценария.
    await state.clear()

    # ============ КНИГА (сразу, без диагностики) ============
    if cat == "cat_book":
        await callback.message.answer(
            f"{intro}\n\n{build_product_card('recipes')}",
            reply_markup=product_keyboard("recipes"),
        )
        await callback.answer()
        return

    # ============ О ТРЕНЕРЕ (сразу) ============
    if cat == "cat_about":
        await callback.message.answer(ABOUT_TRAINER_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return

    # ============ ТРЕНИРОВКИ ============
    if cat == "cat_workouts":
        await state.set_state(Diagnostics.workout_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_WORKOUTS_1}",
            reply_markup=workout_q1_keyboard(),
        )
        await callback.answer()
        return

    # ============ ПИТАНИЕ ============
    if cat == "cat_nutrition":
        await state.set_state(Diagnostics.nutrition_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_NUTRITION_1}",
            reply_markup=nutrition_q1_keyboard(),
        )
        await callback.answer()
        return

    # ============ ГОТОВАЯ СИСТЕМА (один вопрос) ============
    if cat == "cat_system":
        await state.set_state(Diagnostics.system_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO_SHORT}\n\n{Q_SYSTEM_1}",
            reply_markup=system_q1_keyboard(),
        )
        await callback.answer()
        return

    # ============ ОНЛАЙН-ВЕДЕНИЕ ============
    if cat == "cat_online":
        await state.set_state(Diagnostics.online_q1)
        await callback.message.answer(
            f"{intro}\n\n{DIAG_INTRO}\n\n{Q_ONLINE_1}",
            reply_markup=online_q1_keyboard(),
        )
        await callback.answer()
        return

    # Неизвестная категория — подстраховка, чтобы бот не "завис" молча.
    await callback.message.answer(intro, reply_markup=main_menu_keyboard())
    await callback.answer()


# =================== СЦЕНАРИЙ ТРЕНИРОВОК ===================
# Продукт выбирается по проблеме (wq2); цель (wq1) используется в тексте.
@router.callback_query(Diagnostics.workout_q1, F.data.startswith("wq1_"))
async def process_workout_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(goal=callback.data)
    await state.set_state(Diagnostics.workout_q2)
    await callback.message.answer(Q_WORKOUTS_2, reply_markup=workout_q2_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.workout_q2, F.data.startswith("wq2_"))
async def process_workout_q2(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    key, reason = recommend_workout(data.get("goal", ""), callback.data)
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}\n\n<i>{reason}</i>",
        reply_markup=product_keyboard(key),
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ПИТАНИЯ ===================
# Продукт выбирается по проблеме (nq1); цель (nq2) используется в тексте.
@router.callback_query(Diagnostics.nutrition_q1, F.data.startswith("nq1_"))
async def process_nutrition_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(problem=callback.data)
    await state.set_state(Diagnostics.nutrition_q2)
    await callback.message.answer(Q_NUTRITION_2, reply_markup=nutrition_q2_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.nutrition_q2, F.data.startswith("nq2_"))
async def process_nutrition_q2(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    key, reason = recommend_nutrition(data.get("problem", ""), callback.data)
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}\n\n<i>{reason}</i>",
        reply_markup=product_keyboard(key),
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ГОТОВОЙ СИСТЕМЫ ===================
# Один вопрос сразу и однозначно определяет тариф (Комфорт/База).
@router.callback_query(Diagnostics.system_q1, F.data.startswith("sq1_"))
async def process_system_q1(callback: CallbackQuery, state: FSMContext) -> None:
    count = callback.data.removeprefix("sq1_")  # "4" или "12"
    await state.clear()
    key, reason = recommend_system(count)
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key)}\n\n<i>{reason}</i>",
        reply_markup=product_keyboard(key),
    )
    await callback.answer()


# =================== СЦЕНАРИЙ ОНЛАЙН-ВЕДЕНИЯ ===================
# Продукт всегда один (тариф не дробится), но ответы персонализируют текст
# и подсвечивают в карточке самую важную для клиента фичу.
@router.callback_query(Diagnostics.online_q1, F.data.startswith("oq1_"))
async def process_online_q1(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(goal=callback.data)
    await state.set_state(Diagnostics.online_q2)
    await callback.message.answer(Q_ONLINE_2, reply_markup=online_q2_keyboard())
    await callback.answer()


@router.callback_query(Diagnostics.online_q2, F.data.startswith("oq2_"))
async def process_online_q2(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    key, reason, highlight = recommend_online(data.get("goal", ""), callback.data)
    await callback.message.answer(
        f"{RECOMMENDATION_HEADER}\n\n{build_product_card(key, highlight=highlight)}\n\n<i>{reason}</i>",
        reply_markup=product_keyboard(key),
    )
    await callback.answer()
