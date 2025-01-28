from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class User(BaseModel):
    full_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(Text)
    phone_number: Mapped[str] = mapped_column(String(20))


