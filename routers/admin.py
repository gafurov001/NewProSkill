from datetime import datetime, timedelta
from random import randint
from typing import Optional

import jwt
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response

from cache import Cache
from models import Admin
from password_bcrypt import hash_password, verify_password
from schemas import CreateAdmin, PhoneNumberVerify, PhoneNumber, Login, Token
from send_sms import send_sms

admin_router = APIRouter()

cache = Cache()


@admin_router.post("/admin/create/")
async def admin_create(data: CreateAdmin):
    try:
        code = str(randint(120139, 989682))
        sms = send_sms(code, data.phone_number)
        if sms:
            await Admin.create(full_name=data.full_name, role=data.role, username=data.username,
                               password=hash_password(data.password), phone_number=data.phone_number)
            cache.set(data.phone_number, code, 300)
            return Response(status_code=201)
        else:
            return Response("An error occurred while sending the verification code to the phone number.", 422)
    except IntegrityError as e:
        if "UNIQUE constraint" in str(e.orig):
            return Response("This username or phone number already exists.", 409)


@admin_router.post("/phone_number_send/verify_code/")
async def verify_code(data: PhoneNumberVerify):
    code = cache.get(data.phone_number)
    if code == data.code:
        await Admin.update_by_phone(data.phone_number, is_active=True)
        return Response("successfully created!", 201)
    else:
        return Response(status_code=400)


@admin_router.post("/phone_number_send/resend_verify_code/")
async def resend_verify_code(data: PhoneNumber):
    code = str(randint(120139, 989682))
    sms = send_sms(code, data.phone_number)
    if sms:
        cache.set(data.phone_number, code, 300)
        return Response(status_code=201)
    else:
        return Response("An error occurred while sending the verification code to the phone number.", 422)


# Secret key for encoding and decoding JWT
SECRET_KEY = "hb*&kq9`hP@*ufd1i6#%!kjb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Dependency to get the current user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to create a refresh token
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # Default expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify the token and get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")


# Login endpoint to get both access and refresh tokens
@admin_router.post("/login/", response_model=Token)
async def login_for_access_token(user: Login):
    usr = [i for i in await Admin.filter(Admin.phone_number == user.phone_number)]
    # Normally, you would verify the user's credentials here
    if usr:
        usr = usr[0]
        if usr.is_active == True and verify_password(user.password, usr.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            access_token = create_access_token(data={"sub": user.phone_number}, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(data={"sub": user.phone_number}, expires_delta=refresh_token_expires)
            return {"access_token": access_token, "refresh_token": refresh_token, "role": usr.role}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Endpoint to refresh the access token using the refresh token
@admin_router.post("/refresh_token", response_model=Token)
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # Generate a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": phone_number}, expires_delta=access_token_expires)
    usr = [i for i in await Admin.filter(Admin.phone_number == phone_number)]
    if usr:
        usr = usr[0]
        return {"access_token": new_access_token, "refresh_token": refresh_token, "role": usr.role}


# Protected route that requires a valid JWT access token
@admin_router.get("/protected/")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You are authenticated."}

