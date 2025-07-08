from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models.todolist import Category


class CategoryRepository(SQLAlchemySyncRepository[Category]):
    """Repository for managing categories."""

    model_type = Category


async def provide_category_repository(db_session: Session) -> CategoryRepository:
    """Provides an instance of CategoryRepository."""
    return CategoryRepository(session=db_session)
