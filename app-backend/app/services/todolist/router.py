from litestar import Router

from .todos.controllers import TodoController

todolist_router = Router(
    path="/todolist",
    route_handlers=[
        TodoController,
    ],
)
