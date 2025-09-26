from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from core.psql import get_db
from db.psql.crud.crud import get_user_by_telegram_id

router = Router()


@router.message(Command("start"))
async def start_command(msg: Message):
    """
    Обработчик команды /start
    """

    async for db in get_db():
        user = await get_user_by_telegram_id(db, msg.from_user.id)

        if user:

            await show_user_menu(msg)
        else:

            await ask_phone_number(msg)
        break


async def ask_phone_number(msg: Message):
    """
    Запрос номера телефона у нового пользователя
    """
    share_contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await msg.answer(
        "Привет, отправьте ваш номер телефона:",
        reply_markup=share_contact_keyboard
    )


async def show_user_menu(msg: Message):
    """
    Показ меню для зарегистрированного пользователя
    """
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Мои данные", callback_data="my_data")]]
    )

    await msg.answer(
        "Главное меню:",
        reply_markup=keyboard
    )