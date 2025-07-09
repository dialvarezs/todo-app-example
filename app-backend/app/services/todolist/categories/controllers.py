from typing import Any, Sequence

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, Request, Response, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.models.todolist import Category

from .dtos import CategoryCreateDTO, CategoryDTO, CategoryUpdateDTO
from .repositories import CategoryRepository, provide_category_repository


def not_found_error_handler(_: Request[Any, Any, Any], __: NotFoundError) -> Response[Any]:
    return Response(status_code=404, content={"status_code": 404, "detail": "Role not found"})


class CategoryController(Controller):
    path = "/categories"
    tags = ["todolist | categories"]
    return_dto = CategoryDTO
    dependencies = {"categories_repo": Provide(provide_category_repository)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
    }

    @get(path="/", summary="ListCategories")
    async def list(self, categories_repo: CategoryRepository) -> Sequence[Category]:
        """List all categories."""
        return categories_repo.list()

    @get(path="/{category_id:int}", summary="GetCategory")
    async def fetch(self, category_id: int, categories_repo: CategoryRepository) -> Category:
        """Get a category by ID."""
        return categories_repo.get_one(id=category_id)

    @post(path="/", summary="CreateCategory", dto=CategoryCreateDTO)
    async def create(self, data: Category, categories_repo: CategoryRepository) -> Category:
        """Create a new category."""
        return categories_repo.add(data, auto_commit=True)

    @patch(path="/{category_id:int}", summary="UpdateCategory", dto=CategoryUpdateDTO)
    async def update(
        self, category_id: int, data: DTOData[Category], categories_repo: CategoryRepository
    ) -> Category:
        """Update an existing category."""
        category, _ = categories_repo.get_and_update(
            id=category_id,
            **data.as_builtins(),
            match_fields=["id"],
            auto_commit=True,
        )
        return category

    @delete(path="/{category_id:int}", summary="DeleteCategory")
    async def delete(self, category_id: int, categories_repo: CategoryRepository) -> None:
        """Delete a category by ID."""
        categories_repo.delete(category_id)
