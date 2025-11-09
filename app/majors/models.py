from datetime import datetime
from app.database import Base, str_uniq, int_pk, str_null_true
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text

class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    events: Mapped[list["Event"]] = relationship("Event", back_populates='major')
    students: Mapped[list["Student"]] = relationship("Student", back_populates='major')

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    def __repr__(self):
        return str(self)
