from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Здравствуйте! Я QA-ассистент приемной комиссии ИТМО.\n\n"
        "Я могу ответить на ваши вопросы по магистерским программам 'Искусственный интеллект' и 'Искусственный интеллект в управлении продуктом'.\n\n"
        "Просто задайте свой вопрос, например: 'Чем отличаются эти две программы?' или 'Какие сроки подачи документов?'"
    )
