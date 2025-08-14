# app/bot.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.config import load_config
from app.handlers import common, qa_handler
from app.services.yandex_assistant_service import YandexAssistantService

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    config = load_config()

    assistant_service = YandexAssistantService(config)
    bot = Bot(
        token=config.bot_token, 
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp["assistant_service"] = assistant_service
    
    dp.include_router(common.router)
    dp.include_router(qa_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
