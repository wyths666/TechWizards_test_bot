from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from config import cnf
from core.psql import get_db
from db.psql.crud.crud import get_user_by_phone
from api.schemas.user import SendMessageRequest, SendMessageResponse

router = APIRouter(
    tags=["User"],
    prefix="/user"
)


def verify_api_token(x_token: str = Header(..., alias="X-Token")):
    """Проверка статичного токена API"""
    if x_token != cnf.api.TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    return x_token


@router.post("/send-message",
             dependencies=[Depends(verify_api_token)],
             response_model=SendMessageResponse)
async def send_message(
        request: SendMessageRequest,
        db: AsyncSession = Depends(get_db)
) -> SendMessageResponse:
    """
    Отправить сообщение пользователю по номеру телефона
    """

    user = await get_user_by_phone(db, request.phone_number)

    if not user:
        return SendMessageResponse(
            success=False,
            message="Пользователь с таким номером не найден"
        )

    try:
        from core.bot import bot
        await bot.send_message(user.telegram_id, request.text)

        return SendMessageResponse(
            success=True,
            message="Сообщение отправлено",
            user_id=user.telegram_id
        )
    except Exception as e:
        return SendMessageResponse(
            success=False,
            message=f"Ошибка отправки: {str(e)}"
        )