from advanced_alchemy.filters import CollectionFilter
from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models.todolist import Todo
from app.services.todolist.categories.repositories import CategoryRepository


class TodoRepository(SQLAlchemySyncRepository[Todo]):
    """Repository for managing TODO items."""

    model_type = Todo

    def add_with_existing_categories(self, categories_repo: CategoryRepository, todo: Todo):
        """Add a TODO item using existing categories, matching by id."""
        todo.categories = categories_repo.list(
            CollectionFilter(field_name="id", values=[cat.id for cat in todo.categories])
        )
        self.add(todo)

        return todo


async def provide_todo_repository(db_session: Session) -> TodoRepository:
    """Provides an instance of TodoRepository."""
    return TodoRepository(session=db_session)
