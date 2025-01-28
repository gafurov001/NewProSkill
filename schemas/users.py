from pydantic import BaseModel


class CreateUser(BaseModel):
    full_name: str
    username: str
    password: str
    confirm_password: str
    phone_number: str

class CreateAdmin(BaseModel):
    full_name: str
    role: str
    username: str
    password: str
    phone_number: str


class PhoneNumberVerify(BaseModel):
    phone_number: str
    code: str

class PhoneNumber(BaseModel):
    phone_number: str

class Login(BaseModel):
    phone_number: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    role: str
