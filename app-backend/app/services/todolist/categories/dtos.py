from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models.todolist import Category


class CategoryDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig()


class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "todos"},
    )


class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "todos"},
        partial=True,
    )
