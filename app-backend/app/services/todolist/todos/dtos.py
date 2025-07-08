from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.models.todolist import Todo


class TodoDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig()


class TodoCreateDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(
        exclude={"id"},
    )


class TodoUpdateDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(
        exclude={"id"},
        partial=True,
    )
