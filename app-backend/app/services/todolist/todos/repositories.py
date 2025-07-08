from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models.todolist import Todo


class TodoRepository(SQLAlchemySyncRepository[Todo]):
    """Repository for managing TODO items."""
    model_type = Todo


async def provide_todo_repository(db_session: Session) -> TodoRepository:
    """Provides an instance of TodoRepository."""
    return TodoRepository(session=db_session)
