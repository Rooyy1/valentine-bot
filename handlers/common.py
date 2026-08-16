from aiogram import Router, F
from aiogram.types import Message

from data.texts import FALLBACK_TEXT
from keyboards.main import main_menu_keyboard

router = Router()


@router.message(F.text)
async def fallback_message(message: Message) -> None:
    """Любое произвольное сообщение вне сценария — подсказываем пользоваться кнопками."""
    await message.answer(FALLBACK_TEXT, reply_markup=main_menu_keyboard())
