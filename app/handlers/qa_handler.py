from aiogram import Router, F
from aiogram.types import Message
from app.services.yandex_assistant_service import YandexAssistantService

router = Router()

# Этот хендлер будет получать экземпляр YandexAssistantService через middleware или kwargs
@router.message(F.text)
async def handle_question(message: Message, assistant_service: YandexAssistantService):
    # Показываем, что бот "думает"
    thinking_message = await message.answer("Думаю...")
    
    # Получаем ответ от QA-системы
    answer = assistant_service.ask(message.text, message.chat.id)
    
    # Редактируем сообщение с "Думаю..." на реальный ответ
    await thinking_message.edit_text(answer)
