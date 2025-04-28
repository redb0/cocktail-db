"""Модуль работы с коктейлями."""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fasthtml.common import P, Tbody, fill_form, to_xml
from sqlmodel import select
from typing_extensions import Annotated

from app.api.deps import CocktailServiceDep, IngredientServiceDep, SessionDep
from app.core.utils import convert_to_list_int
from app.html_services import CocktailHTMLService
from app.models import Ingredient
from app.models.cocktail import CocktailCreate, CocktailUpdate
from app.models.forms import FiltersFrom, SearchForm

router = APIRouter()


@router.get("", response_class=HTMLResponse)
def get_all_cocktails(
    service: CocktailServiceDep,
    ingredient_service: IngredientServiceDep,
):
    cocktails = service.get_all()
    ingredients = ingredient_service.get_all()
    content = CocktailHTMLService.all_view(cocktails, ingredients)
    return to_xml(content)


@router.post("/search", response_class=HTMLResponse)
def search_cocktail(
    form: Annotated[SearchForm, Form()],
    service: CocktailServiceDep,
):
    # https://gallery.fastht.ml/app/dynamic_user_interface_(htmx)/active_search/
    # https://gallery.fastht.ml/code/dynamic_user_interface_(htmx)/active_search
    cocktails = service.search(form.search)

    return to_xml(
        Tbody(
            *[CocktailHTMLService.row_view(i) for i in cocktails],
            id="cocktail-list",
            hx_swap_oob="true",
        ),
    )


@router.post("/filter", response_class=HTMLResponse)
async def filter_cocktail(
    form: Annotated[FiltersFrom, Form()],
    service: CocktailServiceDep,
):
    cocktails = service.filter_all(form)

    return to_xml(
        Tbody(
            *[CocktailHTMLService.row_view(i) for i in cocktails],
            id="cocktail-list",
            hx_swap_oob="true",
        ),
    )


@router.get("/{item_id:int}", response_class=HTMLResponse)
def get_cocktail(item_id: int, service: CocktailServiceDep):
    cocktail = service.get(item_id)
    if not cocktail:
        return to_xml(P("Коктейль не найден"))

    content = CocktailHTMLService.detail_view(cocktail)
    return to_xml(content)


@router.get("/{item_id:int}/edit", response_class=HTMLResponse)
def edit_cocktail(
    item_id: int,
    cocktail_service: CocktailServiceDep,
    ingredient_service: IngredientServiceDep,
):
    cocktail = cocktail_service.get(item_id)
    if cocktail is None:
        msg = "Доделать ошибку"
        raise ValueError(msg)
    ingredients = ingredient_service.get_all()

    content = CocktailHTMLService.update_view(cocktail, ingredients)
    return to_xml(content)


@router.get("/add/form", response_class=HTMLResponse)
async def get_form(session: SessionDep, request: Request):
    # удаляемый компонент коктейля, если есть
    deleted_id: str | int | None = request.query_params.get("deleted-id")
    if deleted_id is not None:
        deleted_id = int(deleted_id)

    # новый компонент коктейля
    ingredient_name = request.query_params.get("ingredient")
    quantity = request.query_params.get("quantity")

    # уже добавленные компоненты
    ingredients_id = convert_to_list_int(request.query_params.get("ingredients", ""))
    quantities = convert_to_list_int(request.query_params.get("quantities", ""))

    all_ingredients = session.exec(select(Ingredient)).all()
    # NOTE: if i.id для корректной аннотации
    ingredients_map = {i.name: i.id for i in all_ingredients if i.id}

    if not deleted_id:
        if not ingredient_name or not quantity:
            msg = "Доделать"
            raise ValueError(msg)

        if ingredient_name not in ingredients_map:
            # ингридиент не найден
            msg = "Доделать"
            raise ValueError(msg)

        # Добавление нового компонента к уже добавленным ранее
        ingredients_id.append(ingredients_map[ingredient_name])
        quantities.append(int(quantity))
    else:
        if deleted_id in ingredients_id:
            idx = ingredients_id.index(deleted_id)
            ingredients_id.remove(deleted_id)
            quantities.pop(idx)

    ingredients_map_by_id = {i.id: i for i in all_ingredients}

    cocktail_id: str | int | None = request.query_params.get("cocktail-id")
    if cocktail_id:
        cocktail_id = int(cocktail_id)
    else:
        cocktail_id = None

    form = CocktailHTMLService.edit_form(
        ingredients=[i for i in all_ingredients if i.id not in set(ingredients_id)],
        components=list(
            zip([ingredients_map_by_id[i] for i in ingredients_id], quantities)
        ),
        item_id=cocktail_id,
    )

    return to_xml(
        fill_form(
            form,
            {
                "name": request.query_params.get("name"),
                "description": request.query_params.get("description"),
            },
        ),
    )


@router.get("/add", response_class=HTMLResponse)
def get_create_cocktail_form(service: IngredientServiceDep):
    ingredients = service.get_all()

    content = CocktailHTMLService.create_view(ingredients)
    return to_xml(content)


@router.post("", response_class=HTMLResponse)
async def create_cocktail(
    form: Annotated[CocktailCreate, Form()],
    service: CocktailServiceDep,
):
    new_cocktail = service.create(form)
    content = CocktailHTMLService.row_view(new_cocktail, hx_swap="beforeend")
    return to_xml(content)


@router.patch("/{item_id:int}", response_class=HTMLResponse)
async def update_cocktail(
    item_id: int,
    form: Annotated[CocktailUpdate, Form()],
    service: CocktailServiceDep,
):
    cocktail = service.update(item_id, form)
    content = CocktailHTMLService.row_view(cocktail, hx_swap_oob="true")
    return to_xml(content)


@router.delete("/{item_id:int}", response_class=HTMLResponse)
def delete_cocktail(item_id: int, service: CocktailServiceDep):
    service.delete(item_id)
    content = CocktailHTMLService.delete_view(item_id)
    return to_xml(content)
