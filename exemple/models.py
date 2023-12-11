from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Model


class User(Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[Optional[str]] = mapped_column(String(50))
    lists: Mapped[list["TaskList"]] = relationship(
        "TaskList",
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', fullname='{self.fullname}')"


class TaskList(Model):
    __tablename__ = "task_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="list",
        cascade="all, delete",
        passive_deletes=True,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates="lists")

    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}')"


class Task(Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    list_id: Mapped[int] = mapped_column(
        ForeignKey("task_list.id", ondelete="CASCADE")
    )
    list: Mapped["TaskList"] = relationship("TaskList", back_populates="tasks")
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', owner='{self.owner.username}')"
