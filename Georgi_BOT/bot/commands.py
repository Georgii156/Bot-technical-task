from aiogram import Bot
from aiogram.types import BotCommand

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/review", description="Оставить Отзыв"),
        BotCommand(command="/information", description="Информация и Инструкции"),
    ]
    await bot.set_my_commands(commands)