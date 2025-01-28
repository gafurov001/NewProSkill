from enum import Enum

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel
from models.database import CreatedBaseModel

# class Role(str, Enum):
#     super_admin = "super_admin"
#     content_maker = "content_maker"
#     support_manager = "support_manager"

class Admin(BaseModel):
    full_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)