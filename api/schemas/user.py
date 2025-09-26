from pydantic import BaseModel
from api.schemas.response import ResponseBase

class SendMessageRequest(BaseModel):
    phone_number: str
    text: str

class SendMessageResponse(ResponseBase):
    user_id: int | None = None

