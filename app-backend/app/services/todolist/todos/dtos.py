from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models.todolist import Todo


class TodoDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig()


class TodoCreateDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "categories.0.name", "categories.0.description"},
    )


class TodoUpdateDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "categories.0.name", "categories.0.description"},
        partial=True,
    )
