from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from datetime import datetime
from typing_extensions import Self

class SBaseEvent(BaseModel):
    subject: str = Field(..., min_length=5, max_length=300, description='Название предмета, длинна от 5 до 300 символов')
    major_id: int = Field(..., ge=1, description='ID специальности предмета')
    start_time: datetime = Field(..., description='Время начала занятия')
    end_time: datetime = Field(..., description='Время окончания занятия')

    @model_validator(mode='after')
    def time_correctnes(self) -> Self:
        if self.start_time == self.end_time:
            raise ValueError('Занятие длится 0 секунд')

        if self.start_time > self.end_time:
            raise ValueError('Время начала должно предшествовать времени окончания занятия')
        
        return self


class SEvent(SBaseEvent):
    id: int


class SEventAdd(SBaseEvent):
    pass

class SChangeEventTime(SBaseEvent):
    pass