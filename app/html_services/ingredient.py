"""Модуль HTML сервиса для работы с ингредиентами."""

from collections.abc import Sequence

from fasthtml.common import (
    FT,
    H1,
    H3,
    Button,
    Card,
    Dialog,
    Div,
    Form,
    Input,
    Label,
    Main,
    Option,
    P,
    Script,
    Select,
    Table,
    Tbody,
    Td,
    Textarea,
    Th,
    Thead,
    Tr,
    clear,
    fill_form,
)

from app.api.const import CARD_ICON_32, PENCIL_ICON_32, PLUS_ICON_32, TRACH_ICON_32
from app.models import Ingredient
from app.models.enums import IngredientType, TypeABV, UnitMeasurement


class IngredientHTMLService:
    def row_view(self, ingredient: Ingredient, **kwargs) -> FT:
        return Tr(
            Td(P(ingredient.name), id=f"ingredient-name-{ingredient.id}"),
            Td(P(ingredient.abv), id=f"ingredient-abv-{ingredient.id}"),
            Td(P(ingredient.type_), id=f"ingredient-type-{ingredient.id}"),
            Td(P(ingredient.description), id=f"ingredient-description-{ingredient.id}"),
            Td(
                Button(
                    CARD_ICON_32,
                    hx_get=f"/ingredients/{ingredient.id}",
                    data_target="ingredient-modal-read",
                    onclick="toggleModal(event)",
                    hx_swap="none",
                ),
            ),
            Td(
                Button(
                    PENCIL_ICON_32,
                    hx_get=f"/ingredients/{ingredient.id}/edit-form",
                    data_target="ingredient-modal-edit",
                    onclick="toggleModal(event)",
                    hx_swap="none",
                ),
            ),
            Td(
                Button(
                    TRACH_ICON_32,
                    hx_delete=f"/ingredients/{ingredient.id}",
                    hx_swap="none",
                    Class="delete",
                ),
            ),
            id=f"ingredient-{ingredient.id}",
            **kwargs,
        )

    def all_view(self, ingredients: Sequence[Ingredient]) -> FT:
        add_button = Button(
            PLUS_ICON_32,
            data_target="ingredient-modal-add",
            onclick="toggleModal(event)",
            hx_get="/ingredients/create-form",
            hx_swap="none",
            Class="add",
        )

        rows = [self.row_view(i) for i in ingredients]
        head = Thead(
            *map(
                Th,
                (
                    P("Название"),
                    P("Крепость"),
                    P("Тип"),
                    P("Описание"),
                    "",
                    "",
                    add_button,
                ),
            ),
            cls="bg-purple/10",
        )
        content = Card(
            Table(head, Tbody(*rows, id="ingredient-list"), cls="table"),
            footer=Div(id="current-ingredient"),
        )
        read_modal = Dialog(
            Card(id="ingredient-modal-read-card"),
            id="ingredient-modal-read",
        )
        edit_modal = Dialog(
            Card(id="ingredient-modal-edit-card"),
            id="ingredient-modal-edit",
        )
        add_modal = Dialog(
            Card(id="ingredient-modal-add-card"), id="ingredient-modal-add"
        )

        return Main(
            H1("Ингридиенты коктейлей"),
            content,
            read_modal,
            edit_modal,
            add_modal,
            cls="container",
        )

    def edit_form(self, item_id: int | None = None) -> FT:
        if item_id:
            hx_post = None
            hx_patch = f"ingredients/{item_id}"
            data_target_suffix = "edit"
        else:
            hx_post = "ingredients/"
            hx_patch = None
            data_target_suffix = "add"

        form = Form(
            Label("Название", Input(id="name")),
            Label(
                "Крепость",
                Select(
                    Option(
                        "Выберите крепость...",
                        value="",
                    ),
                    *[Option(i.value, value=i.value, id=i.name) for i in TypeABV],
                    id="abv",
                    name="abv",
                ),
                style="width: 100%;",
            ),
            Label(
                "Тип",
                Select(
                    *[
                        Option(i.value, value=i.value, id=i.name)
                        for i in IngredientType
                    ],
                    id="type_",
                    name="type_",
                ),
                style="width: 100%;",
            ),
            Label(
                "Единица измерения",
                Select(
                    *[
                        Option(i.value, value=i.value, id=i.name)
                        for i in UnitMeasurement
                    ],
                    id="unit_measurement",
                    name="unit_measurement",
                ),
                style="width: 100%;",
            ),
            Label(
                "Описание",
                Textarea(
                    placeholder="Введите описание ингредиента...",
                    id="description",
                ),
            ),
            Button(
                "Сохранить",
                autofocus=True,
                data_target=f"ingredient-modal-{data_target_suffix}",
                onclick="toggleModal(event)",
                hx_post=hx_post,
                hx_patch=hx_patch,
                hx_target="#ingredient-list",
                hx_swap="beforeend",
                Class="add",
            ),
            Script(
                code="""
                    new YoSelect(document.querySelector('#abv'), {
                        search: false,
                        creatable: true,
                        placeholder: "Выберите крепость..."
                    });
                    new YoSelect(document.querySelector('#type_'), {search: false,});
                    new YoSelect(document.querySelector('#unit_measurement'), {search: false,});
                """,
            ),
            id=f"ingredient-{data_target_suffix}-form",
        )
        return form

    def detail_view(self, ingredient: Ingredient) -> FT:
        return Card(
            Div(
                P(ingredient.name),
                P(ingredient.abv),
                P(ingredient.type_),
                P(ingredient.description),
            ),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="ingredient-modal-read",
                    onclick="toggleModal(event)",
                ),
                H3(ingredient.name, id="ingredient-name-modal"),
            ),
            footer=Div(
                Button(
                    "Закрыть",
                    autofocus=True,
                    data_target="ingredient-modal-read",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 900px",
            id="ingredient-modal-read-card",
        )

    def create_view(self) -> FT:
        return Card(
            self.edit_form(),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="ingredient-modal-add",
                    onclick="toggleModal(event)",
                ),
                H3("Добавить ингредиент", id="ingredient-name-modal"),
            ),
            footer=Div(
                Button(
                    "Отменить",
                    role="button",
                    cls="secondary",
                    data_target="ingredient-modal-add",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 1000px; max-width: 1000px",
            id="ingredient-modal-add-card",
        )

    def update_view(self, ingredient: Ingredient) -> FT:
        return Card(
            fill_form(self.edit_form(item_id=ingredient.id), ingredient),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="ingredient-modal-edit",
                    onclick="toggleModal(event)",
                ),
                H3("Изменить ингредиент", id="ingredient-name-modal"),
            ),
            footer=Div(
                Button(
                    "Отменить",
                    role="button",
                    cls="secondary",
                    data_target="ingredient-modal-edit",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 1000px; max-width: 1000px",
            id="ingredient-modal-edit-card",
        )

    def delete_view(self, item_id: int) -> FT:
        return clear(f"ingredient-{item_id}")
