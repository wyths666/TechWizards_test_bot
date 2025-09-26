from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


from core.psql import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), comment="Номер телефона")  # Изменил phone на phone_number
    first_name: Mapped[str] = mapped_column(String(100))  # Изменил full_name на first_name (по заданию)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # Убрал поле role - по заданию не нужно