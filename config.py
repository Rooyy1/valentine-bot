import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Юзернейм тренера — используется в кнопке финального CTA
TRAINER_USERNAME = os.getenv("TRAINER_USERNAME", "Krismihalchampion_wff_wbb")

# file_id фотографии тренера. ВНИМАНИЕ: file_id привязан к конкретному боту,
# который изначально принял это фото. Если вы используете другой токен бота,
# этот file_id может не сработать — бот в таком случае автоматически
# отправит приветствие без фото (см. handlers/start.py). Чтобы фото
# показывалось, отправьте это же фото вашему боту и подставьте новый file_id.
TRAINER_PHOTO_ID = os.getenv(
    "TRAINER_PHOTO_ID",
    "AgACAgIAAxkBAAOfaoGO9C7Jlj6k-PdZRm5b-UmTvRIAAsgbaxvkSxFILc_i02UkzW8BAAMCAAN5AAM9BA",
)

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не задан. Скопируйте .env.example в .env и укажите токен, "
        "полученный у @BotFather."
    )
