from fastapi import APIRouter, Depends, HTTPException, status
from app.students.dependencies import get_current_user_student
from app.students.service import StudentService
from app.students.schemas import SStudent, SStudentAdd
from app.students.rb import RBStudent, RBUserTimetable
from app.events.service import EventsService
from datetime import date

router = APIRouter(prefix='/students', tags=['Работа со студентами'])

@router.get('/', summary='Получить всех студентов')
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentService.find_all(**request_body.to_dict())


@router.get('/{student_id}', summary='Получить одного студента по id')
async def get_student_by_id(student_id: int) -> SStudent | None:
    res = await StudentService.find_full_data(student_id)
    if res is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    return res


@router.get('/by_filter', summary='Получить одного студента по фильтру')
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | None:
    res = await StudentService.get_one_or_none(**request_body.to_dict())
    if res is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return res


@router.post('/add/')
async def add_student(student: SStudentAdd) -> dict:
    check = await StudentService.add(**student.model_dump())
    if check:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}
    

@router.delete("/dell/{student_id}")
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentService.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}


@router.get('/timetable')
async def get_timetable(date_: RBUserTimetable = Depends(), user = Depends(get_current_user_student)):
    student = await StudentService.get_one_or_none(first_name=user.first_name, last_name=user.last_name)
    if student is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Записи о студенте {user.first_name} {user.last_name} не найдены')
    
    return await EventsService.get_events_for_date(
        major_id=student.major_id,
        date=date(day=date_.day, month=date_.month, year=date_.year))