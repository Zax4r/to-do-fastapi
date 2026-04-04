from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String, Integer
from typing import List


class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(256))
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0)
    active_tasks: Mapped[int] = mapped_column(Integer, default=0)

    tasks: Mapped[List['Task']] = relationship('Task',back_populates='user',cascade="all, delete-orphan")


