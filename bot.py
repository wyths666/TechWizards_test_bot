import asyncio
from aiogram import Bot, Dispatcher
from config import cnf

from bot.handlers.user import commands, reg


async def main():
    bot = Bot(token=cnf.bot.TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(reg.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())