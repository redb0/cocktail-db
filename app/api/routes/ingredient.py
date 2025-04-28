"""Модуль работы с ингредиентами."""

from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from fasthtml.common import P, to_xml
from typing_extensions import Annotated

from app.api.deps import IngredientServiceDep
from app.html_services import IngredientHTMLService
from app.models.ingredient import IngredientCreate, IngredientUpdate

router = APIRouter()


@router.get("", response_class=HTMLResponse)
def get_all_ingredients(service: IngredientServiceDep):
    """Сформировать HTML для просмотра всех ингредиентов."""
    ingredients = service.get_all()
    content = IngredientHTMLService().all_view(ingredients)
    return to_xml(content)


@router.get("/{item_id:int}", response_class=HTMLResponse)
def get_ingredient(item_id: int, service: IngredientServiceDep):
    """Сформировать HTML для просмотра ингредиента по ID."""
    ingredient = service.get(item_id)
    if not ingredient:
        return to_xml(P("Коктейль не найден"))

    content = IngredientHTMLService().detail_view(ingredient)
    return to_xml(content)


@router.get("/create-form", response_class=HTMLResponse)
def get_create_ingredient_form():
    """Сформировать HTML формы для создания ингредиента."""
    content = IngredientHTMLService().create_view()
    return to_xml(content)


@router.post("", response_class=HTMLResponse)
def create_ingredient(
    ingredient_data: Annotated[IngredientCreate, Form()],
    service: IngredientServiceDep,
):
    """Создать новый ингредиент."""
    ingredient = service.create(ingredient_data)

    content = IngredientHTMLService().row_view(ingredient, hx_swap="beforeend")
    return to_xml(content)


@router.get("/{item_id:int}/edit-form", response_class=HTMLResponse)
def get_edit_ingredient_form(item_id: int, service: IngredientServiceDep):
    """Сформировать HTML формы для обновления ингредиента."""
    ingredient = service.get(item_id)
    if ingredient is None:
        msg = "Доделать"
        raise ValueError(msg)

    content = IngredientHTMLService().update_view(ingredient)
    return to_xml(content)


@router.patch("/{item_id:int}", response_class=HTMLResponse)
def update_ingredient(
    item_id: int,
    ingredient_data: Annotated[IngredientUpdate, Form()],
    service: IngredientServiceDep,
):
    """Обновить существующий ингредиент по ID."""
    ingredient = service.update(item_id, ingredient_data)

    content = IngredientHTMLService().row_view(ingredient, hx_swap_oob="true")
    return to_xml(content)


@router.delete("/{item_id:int}", response_class=HTMLResponse)
def delete_ingredient(item_id: int, service: IngredientServiceDep):
    """Удалить ингредиент по ID."""
    # TODO: Проверка на участие в коктейлях
    service.delete(item_id)
    content = IngredientHTMLService().delete_view(item_id)
    return to_xml(content)
