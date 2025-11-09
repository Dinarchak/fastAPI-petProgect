from sqlalchemy import delete, select, update, event
from app.majors.models import Major
from app.students.models import Student
from app.service.base import BaseService
from app.database import async_session_maker
from sqlalchemy.orm import joinedload
from app.students.schemas import SStudent

class StudentService(BaseService):
    model = Student

    @classmethod
    async def find_all(cls, **filter_by) -> list[SStudent]:
        async with async_session_maker() as session:
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(**filter_by)
            result_student = await session.execute(query_student)
            students_list = result_student.scalars().all()

            return [SStudent(**(student.to_dict() | {'major': student.major.major_name})) for student in students_list]



    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result_student = await session.execute(query_student)
            student_info = result_student.scalar_one_or_none()

            if student_info is None:
                return None

            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name

            return student_data
        
    @classmethod
    async def add_student(cls, student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id
            
    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()
    
                if not student_to_delete:
                    return None
    
                # Удаляем студента
                await session.execute(
                    delete(cls.model).filter_by(id=student_id)
                )
    
                await session.commit()
                return student_id


    @event.listens_for(Student, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students + 1)
        )

    @event.listens_for(Student, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students - 1)
        )
