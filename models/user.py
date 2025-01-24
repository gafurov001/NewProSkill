from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class User(BaseModel):
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(Text)


