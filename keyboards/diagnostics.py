from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def _with_back(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


# =================== ТРЕНИРОВКИ ===================
def workout_q1_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔥 Похудение", callback_data="wq1_loss")
    builder.button(text="💪 Набор массы", callback_data="wq1_mass")
    builder.button(text="⚖️ Тонус и форма", callback_data="wq1_tone")
    return _with_back(builder)


def workout_q2_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📐 Хромает техника", callback_data="wq2_tech")
    builder.button(text="🤔 Не знаю программу", callback_data="wq2_program")
    builder.button(text="😫 Нет прогресса", callback_data="wq2_progress")
    return _with_back(builder)


# =================== ПИТАНИЕ ===================
def nutrition_q1_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🍔 Сложно отказаться от вредного", callback_data="nq1_junk")
    builder.button(text="📉 Не понимаю КБЖУ", callback_data="nq1_kbju")
    builder.button(text="🤷 Не знаю, что готовить", callback_data="nq1_meals")
    return _with_back(builder)


def nutrition_q2_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📉 Хочу сбросить вес", callback_data="nq2_loss")
    builder.button(text="🍽 Хочу наладить привычки", callback_data="nq2_habits")
    return _with_back(builder)


# =================== ГОТОВАЯ СИСТЕМА (один вопрос) ===================
def system_q1_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🛋️ 4 тренировки с тренером (Комфорт)", callback_data="sq1_4")
    builder.button(text="🏆 12 тренировок с тренером (База)", callback_data="sq1_12")
    return _with_back(builder)


# =================== ОНЛАЙН-ВЕДЕНИЕ ===================
def online_q1_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📉 Хочу похудеть", callback_data="oq1_loss")
    builder.button(text="💪 Хочу рельеф", callback_data="oq1_mass")
    builder.button(text="⚖️ Хочу тонус", callback_data="oq1_tone")
    return _with_back(builder)


def online_q2_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Поддержка 24/7", callback_data="oq2_support")
    builder.button(text="🎥 Разбор техники по видео", callback_data="oq2_video")
    builder.button(text="📋 Готовая программа", callback_data="oq2_program")
    return _with_back(builder)
