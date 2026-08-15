```python
import asyncio
import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import TRAINER_PHOTO_ID
from data.texts import MAIN_MENU_PROMPT, WELCOME_WITH_STORY_1, WELCOME_WITH_STORY_2
from keyboards.main import main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await send_welcome_parts(message)


async def send_welcome_parts(message: Message) -> None:
    # Первое сообщение — фото + начало истории
    try:
        await message.answer_photo(
            photo=TRAINER_PHOTO_ID,
            caption=WELCOME_WITH_STORY_1
        )
    except TelegramBadRequest:
        logger.warning("Не удалось отправить фото, отправляю без фото.")
        await message.answer(WELCOME_WITH_STORY_1)

    # Небольшая пауза, чтобы сообщения не сливались
    await asyncio.sleep(1)

    # Вторая часть истории
    await message.answer(WELCOME_WITH_STORY_2)

    # И только после истории показываем меню
    await asyncio.sleep(1)
    await message.answer(
        MAIN_MENU_PROMPT,
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer(
        MAIN_MENU_PROMPT,
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()
```
