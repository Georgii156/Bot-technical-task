import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import router
from bot.config import TOKEN
from bot.db_creation import init_db
from bot.commands import set_bot_commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    session = AiohttpSession()
    
    bot = Bot(
        token=TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    await init_db()
    await set_bot_commands(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot closed")

if __name__ == "__main__":
    asyncio.run(main())
