from sqlalchemy import DateTime, text
from sqlalchemy.orm import mapped_column, Mapped
from typing import Annotated
from datetime import datetime

intpk = Annotated[
    int,
    mapped_column(primary_key=True)
]

created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())")
    )
]

str_32 = Annotated[str, 32]
str_128 = Annotated[str, 128]