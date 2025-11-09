from fastapi import APIRouter, HTTPException, Response, status, Depends
from app.users.auth import get_password_hash
from app.users.dependencies import get_current_admin_user
from app.users.service import UsersService, RolesService
from app.users.schemas import SUserRegister, SUserAuth
from app.users.models import User
from app.users.dependencies import get_current_user, validate_refresh_token
from app.users.auth import create_token, authenticate_user
from app.config import Settings

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register/')
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersService.get_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersService.add(**user_dict)
    return {'message': 'Вы успешно зарегестрировались!'}

@router.post('/login/')
async def auth_user(response: Response, user_data: SUserAuth) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль')
    
    access_token = create_token({
        'sub': str(check.id),
        'type': 'access'},
        Settings.ACCESS_TOKEN_EXP
    )
    refresh_token = create_token({
        'sub': str(check.id),
        'type': 'refresh'},
        Settings.REFRESH_TOKEN_EXP
    )

    response.set_cookie(key='users_access_token', value=access_token, httponly=True)
    response.set_cookie(key='users_refresh_token', value=refresh_token, httponly=True)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_token(key='users_access_toke')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.post('/refresh')
async def refresh_token(response: Response, check = Depends(validate_refresh_token)):
    new_access_token = create_token({
        'sub': str(check.id),
        'type': 'access'},
        Settings.ACCESS_TOKEN_EXP
    )
    new_refresh_token = create_token({
        'sub': str(check.id),
        'type': 'refresh'},
        Settings.REFRESH_TOKEN_EXP
    )

    response.set_cookie(key='users_access_token', value=new_access_token, httponly=True)
    response.set_cookie(key='users_refresh_token', value=new_refresh_token, httponly=True)

    return {'access_token': new_access_token, 'refresh_token': new_refresh_token}

@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersService.find_all()

@router.post('roles/create_role/', tags=['Работа с ролями'])
async def create_new_role(name: str):
    check = await RolesService.add(role_name=name)
    if check:
        return {'message': f'Роль {name} создана'}
    else:
        return {'message': f'Ошибка при добавлении роли'}

@router.delete('/delete_role/', tags=['Работа с ролями'])
async def delete_role(role_id: int):
    check = await RolesService.delete(id=role_id)
    if check:
        return {'message': f'Роль c id {role_id} удалена'}
    return {'message': 'Ошибка при удалении роли'}

@router.get('/roles', tags=['Работа с ролями'])
async def get_all_roles():
    return await RolesService.find_all()
