from fastapi import Depends, status, HTTPException
from app.users.models import User
from app.users.service import UsersService, RolesService
from app.users.auth import get_auth_data
from jose import JWTError, jwt
from datetime import datetime, timezone
from app.users.auth import get_token, get_refresh_token

async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
    
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    
    user = await UsersService.get_by_id_or_none(int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    return user
    

async def get_current_admin_user(current_user: User = Depends(get_current_user)):

    admin_role = await RolesService.get_one_or_none(role_name='ADMIN')
    super_admin_role = await RolesService.get_one_or_none(role_name='SUPER_ADMIN')

    if current_user.role == admin_role.id or current_user.role == super_admin_role.id:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def validate_refresh_token(token = Depends(get_refresh_token)):
    auth_data = get_auth_data()
    try:
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if not expire or expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    
    user = await UsersService.get_by_id_or_none(int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
        