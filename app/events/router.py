from fastapi import APIRouter, Depends
from app.events.schemas import SEventAdd, SChangeEventTime
from app.events.rb import RBEvent
from app.events.service import EventsService

router = APIRouter(prefix='/events', tags=['Работа с занятиями'])

@router.get('/', summary='Получить все занятия')
async def get_all_events(request_body: RBEvent = Depends()):
    return await EventsService.find_all(**request_body.to_dict())

@router.post('/add/', summary='Создать занятие')
async def add_event(event: SEventAdd) -> dict:
    check = await EventsService.add(**event.model_dump())
    if check:
        return {'message': 'Занятие создано успешно!', 'event': event}
    else:
        return {'message': 'Ошибка создания занятия!'}
    
@router.put('/change_time/', summary='Изменить время проведения')
async def change_time(event: SChangeEventTime) -> dict:
    check = await EventsService.update(
        filter_by={'major_id': event.major_id, 'subject': event.subject},
        start_time=event.start_time,
        end_time=event.end_time
    )

    if check:
        return {'message': 'Время проведения занятия изменено', 'event': event}
    else:
        return {'message': 'При изменении времени проведения возникла ошибка!'}
    
@router.delete('/delete/', summary='Отменить занятие')
async def delete_event(event_id: int) -> dict:
    check = await EventsService.delete(id=event_id)
    if check:
        return {"message": f"Занятие с ID {event_id} удален!"}
    else:
        return {"message": "Ошибка при удалении занятия!"}