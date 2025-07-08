from advanced_alchemy.base import BigIntBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Todo(BigIntBase):
    """TODO item model."""

    __tablename__ = "todolist_todos"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)

    categories: Mapped[list["Category"]] = relationship(
        back_populates="todos", secondary="todolist_todos_categories"
    )


class Category(BigIntBase):
    """Category model for organizing TODO items."""

    __tablename__ = "todolist_categories"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    todos: Mapped[list["Todo"]] = relationship(
        back_populates="categories", secondary="todolist_todos_categories"
    )


class TodoCategory(BigIntBase):
    """Association table for many-to-many relationship between TODOs and Categories."""

    __tablename__ = "todolist_todos_categories"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todolist_todos.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("todolist_categories.id"), primary_key=True)
