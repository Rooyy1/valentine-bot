import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import TRAINER_PHOTO_ID
from data.texts import MAIN_MENU_PROMPT, TRAINER_STORY, WELCOME_CAPTION
from keyboards.main import main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await send_welcome(message)


async def send_welcome(message: Message) -> None:
    try:
        await message.answer_photo(photo=TRAINER_PHOTO_ID, caption=WELCOME_CAPTION)
    except TelegramBadRequest:
        # file_id может быть недействителен для этого бота (см. config.py) —
        # не роняем сценарий, а просто продолжаем текстом.
        logger.warning("Не удалось отправить фото тренера по file_id, отправляю без фото.")
        await message.answer(WELCOME_CAPTION)

    await message.answer(TRAINER_STORY)
    await message.answer(MAIN_MENU_PROMPT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        await callback.message.edit_text(MAIN_MENU_PROMPT, reply_markup=main_menu_keyboard())
    except TelegramBadRequest:
        await callback.message.answer(MAIN_MENU_PROMPT, reply_markup=main_menu_keyboard())
    await callback.answer()
