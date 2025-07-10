from typing import Any, Sequence

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, Request, Response, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.models.todolist import Todo

from ..categories.repositories import CategoryRepository, provide_category_repository
from .dtos import TodoCreateDTO, TodoDTO, TodoUpdateDTO
from .repositories import TodoRepository, provide_todo_repository


def not_found_error_handler(_: Request[Any, Any, Any], __: NotFoundError) -> Response[Any]:
    return Response(status_code=404, content={"status_code": 404, "detail": "Role not found"})


class TodoController(Controller):
    path = "/todos"
    tags = ["todolist | todos"]
    return_dto = TodoDTO
    dependencies = {"todos_repo": Provide(provide_todo_repository)}
    exception_handlers = {NotFoundError: not_found_error_handler}

    @get(path="/", summary="ListTodos")
    async def list(self, todos_repo: TodoRepository) -> Sequence[Todo]:
        """List all TODO items."""
        return todos_repo.list()

    @get(path="/{todo_id:int}", summary="GetTodo")
    async def fetch(self, todo_id: int, todos_repo: TodoRepository) -> Todo:
        """Get a TODO item by ID."""
        return todos_repo.get_one(id=todo_id)

    @post(
        path="/",
        summary="CreateTodo",
        dto=TodoCreateDTO,
        dependencies={"categories_repo": Provide(provide_category_repository)},
    )
    async def create(
        self,
        data: Todo,
        todos_repo: TodoRepository,
        categories_repo: CategoryRepository,
    ) -> Todo:
        """Create a new TODO item."""
        return todos_repo.add_with_existing_categories(categories_repo, data, auto_commit=True)

    @patch(
        path="/{todo_id:int}",
        summary="UpdateTodo",
        dto=TodoUpdateDTO,
        dependencies={"categories_repo": Provide(provide_category_repository)},
    )
    async def update(
        self,
        todo_id: int,
        data: DTOData[Todo],
        todos_repo: TodoRepository,
        categories_repo: CategoryRepository,
    ) -> Todo:
        """Update an existing TODO item."""
        return todos_repo.update_with_existing_categories(
            categories_repo,
            todo_id,
            data,
            auto_commit=True,
        )

    @delete(path="/{todo_id:int}", summary="DeleteTodo")
    async def delete(self, todo_id: int, todos_repo: TodoRepository) -> None:
        """Delete a TODO item by ID."""
        todos_repo.delete(todo_id, auto_commit=True)
