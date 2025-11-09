from fastapi import APIRouter, Depends
from app.majors.schemas import SMajorAdd, SMajorUpdDesc
from app.majors.service import MajorsService
from app.majors.rb import RBMajors

router = APIRouter(prefix='/majors', tags=['Работы с факультетами'])


@router.post('/add/', summary='Добавить новое направление')
async def register_major(major: SMajorAdd) -> dict:
    check = await MajorsService.add(**major.model_dump())
    if check:
        return {'message': 'Факультет успешно добавлен!', 'major': major}
    else:
        return {'message': 'Ошибка при  добавлении факультета!'}
    

@router.put('/update_description/', summary='Обновить описание направления')
async def update_major_description(major: SMajorUpdDesc) -> dict:
    check = await MajorsService.update(
        filter_by={'major_name': major.major_name},
        major_description=major.major_description)
    
    if check:
        return {"message": "Описание факультета успешно обновлено!", "major": major}
    else:
        return {"message": "Ошибка при обновлении описания факультета!"}



@router.get('/', summary='Получить все направления')
async def get_all_students(request_body: RBMajors = Depends()):
    return await MajorsService.find_all(**request_body.to_dict())


@router.delete("/delete/{major_id}", summary='Удалить направление')
async def delete_major(major_id: int) -> dict:
    check = await MajorsService.delete(id=major_id)
    if check:
        return {"message": f"Факультет с ID {major_id} удален!"}
    else:
        return {"message": "Ошибка при удалении факультета!"}