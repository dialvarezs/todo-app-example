from advanced_alchemy.filters import CollectionFilter
from advanced_alchemy.repository import SQLAlchemySyncRepository
from litestar.dto import DTOData
from sqlalchemy.orm import Session

from app.models.todolist import Todo
from app.services.todolist.categories.repositories import CategoryRepository


class TodoRepository(SQLAlchemySyncRepository[Todo]):
    """Repository for managing TODO items."""

    model_type = Todo

    def add_with_existing_categories(self, categories_repo: CategoryRepository, todo: Todo, **kwargs) -> Todo:
        """Add a TODO item using existing categories, matching by id."""
        todo.categories = categories_repo.list(
            CollectionFilter(field_name="id", values=[cat.id for cat in todo.categories])
        )
        self.add(todo, **kwargs)

        return todo

    def update_with_existing_categories(
        self, categories_repo: CategoryRepository, todo_id: int, todo_data: DTOData[Todo], **kwargs) -> Todo:
        """Update a TODO item using existing categories, matching by id."""
        todo_data_dict = todo_data.as_builtins()
        if "categories" in todo_data_dict:
            todo_data_dict["categories"] = categories_repo.list(
            CollectionFilter(field_name="id", values=[cat.id for cat in todo_data_dict["categories"]])
        )
        todo, _ = self.get_and_update(
            id=todo_id, **todo_data_dict, match_fields=["id"], **kwargs
        )

        return todo


async def provide_todo_repository(db_session: Session) -> TodoRepository:
    """Provides an instance of TodoRepository."""
    return TodoRepository(session=db_session)
