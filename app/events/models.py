from app.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime

class Event(Base):
    id: Mapped[int_pk]
    subject: Mapped[str_uniq]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False)

    major: Mapped["Major"] = relationship("Major", back_populates='events')

    def __str__(self):
        return f'Занятие {self.subject} на факультете {self.major.major_name}'
    
    def __repr__(self):
        return f'Event(subject={self.subject}, major={self.major.major_name})'
