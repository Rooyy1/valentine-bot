from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def _with_back(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


# --- ТРЕНИРОВКИ (Вопрос 1) ---
def workouts_goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔥 Похудение", callback_data="wgoal_loss")
    builder.button(text="💪 Набор массы", callback_data="wgoal_mass")
    builder.button(text="⚖️ Тонус и форма", callback_data="wgoal_tone")
    return _with_back(builder)


# --- ТРЕНИРОВКИ (Вопрос 2) ---
def workouts_problem_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📐 Не уверен в технике", callback_data="wprob_technique")
    builder.button(text="🤔 Не знаю, как строить программу", callback_data="wprob_program")
    builder.button(text="😫 Нет прогресса", callback_data="wprob_progress")
    return _with_back(builder)


# --- ПИТАНИЕ (Вопрос 1) ---
def nutrition_problem_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🍔 Не могу отказаться от вредного", callback_data="nprob_junk")
    builder.button(text="📉 Не понимаю КБЖУ", callback_data="nprob_kbju")
    builder.button(text="🤷 Не знаю, что готовить", callback_data="nprob_meals")
    return _with_back(builder)


# --- ПИТАНИЕ (Вопрос 2) ---
def nutrition_goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📉 Хочу сбросить вес и подсушиться", callback_data="ngoal_result")
    builder.button(text="🍽 Хочу наладить привычки", callback_data="ngoal_habits")
    return _with_back(builder)


# --- ГОТОВАЯ СИСТЕМА (Вопрос 1) ---
def system_frequency_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🤝 Хочу с тренером каждую тренировку", callback_data="sfreq_full")
    builder.button(text="🔄 Готов часть тренировок делать сам", callback_data="sfreq_partial")
    return _with_back(builder)


# --- ГОТОВАЯ СИСТЕМА (Вопрос 2) ---
def system_budget_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 До 12 000 ₽", callback_data="sbud_medium")
    builder.button(text="💎 Готов инвестировать 23 000 ₽", callback_data="sbud_high")
    return _with_back(builder)