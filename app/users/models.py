from __future__ import annotations
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk

class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    role: Mapped['Role'] = relationship('Role', back_populates='users')
    extend_existing = True

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'
    

class Role(Base):
    id: Mapped[int_pk]
    role_name: Mapped[str_uniq]

    users: Mapped[list['User']] = relationship('User', back_populates='role')
