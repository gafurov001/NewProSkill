from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.util import await_only
from starlette.responses import Response

from config import conf
from models import User, Admin
from password_bcrypt import hash_password
from schemas import CreateUser

auth_router = APIRouter()


@auth_router.post("/register")
async def say_hello(data: CreateUser):
    if data.password != data.confirm_password:
        return Response("Password and confirm password do not match.", 400)
    usr = [i for i in await User.filter(User.username == data.username)]
    await User.create(full_name=data.full_name, username=data.username, password=hash_password(data.password),
                      phone_number=data.phone_number)
    return



