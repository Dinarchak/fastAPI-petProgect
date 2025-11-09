from app.service.base import BaseService
from app.events.models import Event
from datetime import date, datetime
from app.database import async_session_maker
from sqlalchemy import select

class EventsService(BaseService):
    model = Event
    
    @classmethod
    async def get_events_for_date(cls, major_id: int, date: date):
        async with async_session_maker() as session:

            start_dt = datetime.combine(date, datetime.min.time())  # 00:00:00
            end_dt = datetime.combine(date, datetime.max.time())    # 23:59:59.999999

            query_events = select(cls.model).where(
                cls.model.major_id==major_id,
                cls.model.start_time >= start_dt,
                cls.model.end_time <= end_dt)
            
            result = await session.execute(query_events)
            return result.scalars().all()