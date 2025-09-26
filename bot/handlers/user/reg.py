from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from core.psql import get_db
from db.psql.crud.crud import create_user, get_user_by_telegram_id

router = Router()


@router.message(F.contact)
async def contact_handler(message: Message):
    """
    Обработка отправленного номера телефона
    """
    contact = message.contact


    async for db in get_db():
        user = await create_user(
            db=db,
            telegram_id=message.from_user.id,
            phone_number=contact.phone_number,
            first_name=message.from_user.first_name or "",
            username=message.from_user.username or ""
        )
        break


    await message.answer(
        "Данные приняты. Спасибо!",
        reply_markup=None
    )

    # Показываем кнопку "Мои данные"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Мои данные", callback_data="my_data")]]
    )

    await message.answer("Главное меню:", reply_markup=keyboard)


@router.callback_query(F.data == "my_data")
async def my_data_callback(callback: CallbackQuery):
    """
    Показ данных пользователя
    """
    async for db in get_db():
        user = await get_user_by_telegram_id(db, callback.from_user.id)

        if user:
            text = (
                f"✅ Ваши данные:\n\n"
                f"🆔 TG ID: {user.telegram_id}\n"
                f"📞 Телефон: {user.phone_number}\n"
                f"👤 Имя: {user.first_name}\n"
                f"👤 Юзернейм: @{user.username or 'нет'}\n"
                f"📅 Дата регистрации: {user.created_at.strftime('%d.%m.%Y %H:%M')}"
            )

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="main_menu")]]
            )

            await callback.message.edit_text(text, reply_markup=keyboard)
        break

    await callback.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    """
    Возврат в главное меню
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Мои данные", callback_data="my_data")]]
    )

    await callback.message.edit_text("Главное меню:", reply_markup=keyboard)
    await callback.answer()