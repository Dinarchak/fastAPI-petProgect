from fastapi import Depends, HTTPException, status

from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.service import RolesService


async def get_current_user_student(current_user: User = Depends(get_current_user)):

    student_role = await RolesService.get_one_or_none(role_name='ADMIN')

    if current_user.role == student_role.id:
        return current_user
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Метод только для студентов!')