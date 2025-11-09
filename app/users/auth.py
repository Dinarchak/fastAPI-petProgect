from passlib.context import CryptContext

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from pydantic import EmailStr
from app.config import get_auth_data
from app.users.service import UsersService

from fastapi import Request, HTTPException, status, Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str: # хеширует пароль
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool: # проверить пароль
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, exparatoin: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=exparatoin)
    to_encode.update({'exp': expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersService.get_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

def get_refresh_token(request: Request):
    token = request.cookies.get('users_refresh_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token