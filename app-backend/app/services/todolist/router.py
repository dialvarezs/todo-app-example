from litestar import Router

from .categories.controllers import CategoryController
from .todos.controllers import TodoController

todolist_router = Router(
    path="/todolist",
    route_handlers=[
        TodoController,
        CategoryController,
    ],
)
