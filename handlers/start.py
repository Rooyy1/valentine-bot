import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import TRAINER_PHOTO_ID
from data.texts import WELCOME_TEXT, MAIN_MENU_PROMPT
from keyboards.main import main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await send_welcome(message)


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext) -> None:
    """Позволяет вернуться в главное меню в любой момент, не только по кнопке."""
    await state.clear()
    await message.answer(MAIN_MENU_PROMPT, reply_markup=main_menu_keyboard())


async def send_welcome(message: Message) -> None:
    # Одно цельное приветственное сообщение: фото + весь текст.
    # Если TRAINER_PHOTO_ID пустой или невалидный для текущего бота — не падаем,
    # а тихо отправляем текст без фото.
    if TRAINER_PHOTO_ID:
        try:
            await message.answer_photo(
                photo=TRAINER_PHOTO_ID,
                caption=WELCOME_TEXT,
                reply_markup=main_menu_keyboard(),
            )
            return
        except TelegramBadRequest:
            logger.warning("Не удалось отправить фото, отправляю приветствие без фото.")

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer(MAIN_MENU_PROMPT, reply_markup=main_menu_keyboard())
    await callback.answer()
