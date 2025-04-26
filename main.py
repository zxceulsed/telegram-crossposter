import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.config import config
from src.handlers import router as handlers_router

async def main():

    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем единый роутер, в котором уже есть admin и repost
    dp.include_router(handlers_router)

    # Удаляем старые вебхуки и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
