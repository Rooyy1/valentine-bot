from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def _with_back(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="⬅️ В начало", callback_data="back_main")
    builder.adjust(1)
    return builder.as_markup()


def goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔥 Похудение", callback_data="goal_loss")
    builder.button(text="💪 Набор массы / рельеф", callback_data="goal_mass")
    builder.button(text="⚖️ Тонус и форма", callback_data="goal_tone")
    builder.button(text="🏆 Подготовка к соревнованиям", callback_data="goal_competition")
    return _with_back(builder)


def problem_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🤔 Не знаю, как тренироваться", callback_data="problem_training")
    builder.button(text="🍽 Не могу наладить питание", callback_data="problem_nutrition")
    builder.button(text="📐 Хромает техника выполнения", callback_data="problem_technique")
    builder.button(text="📉 Нет контроля и результата", callback_data="problem_control")
    return _with_back(builder)


def format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏋️ Разовая тренировка в зале", callback_data="format_onetime")
    builder.button(text="📋 Программа + питание, занимаюсь сам(а)", callback_data="format_selfmade")
    builder.button(text="💻 Полное сопровождение онлайн", callback_data="format_online")
    builder.button(text="🤝 Регулярные тренировки с тренером в зале", callback_data="format_inperson")
    return _with_back(builder)