"""Модуль HTML сервиса для работы с коктейлями."""

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
    Grid,
    Hidden,
    Input,
    Label,
    Li,
    Main,
    NotStr,
    Option,
    P,
    Script,
    Search,
    Select,
    Table,
    Tbody,
    Td,
    Textarea,
    Th,
    Thead,
    Tr,
    Ul,
    clear,
    fill_form,
)

from app.api.const import CARD_ICON_32, PENCIL_ICON_32, PLUS_ICON_32, TRACH_ICON_32
from app.models import Cocktail, Ingredient


class CocktailHTMLService:
    @classmethod
    def row_view(cls, cocktail: Cocktail, **kwargs) -> FT:
        return Tr(
            Td(P(cocktail.name), id=f"cocktail-name-{cocktail.id}"),
            Td(P(cocktail.description), id=f"cocktail-description-{cocktail.id}"),
            Td(
                Button(
                    CARD_ICON_32,
                    hx_get=f"/cocktails/{cocktail.id}",
                    data_target="cocktail-modal-read",
                    onclick="toggleModal(event)",
                    hx_swap="none",
                ),
            ),
            Td(
                Button(
                    PENCIL_ICON_32,
                    hx_get=f"/cocktails/{cocktail.id}/edit",
                    data_target="cocktail-modal-edit",
                    onclick="toggleModal(event)",
                    hx_swap="none",
                ),
            ),
            Td(
                Button(
                    TRACH_ICON_32,
                    hx_delete=f"/cocktails/{cocktail.id}",
                    hx_swap="none",
                    Class="delete",
                ),
            ),
            id=f"cocktail-{cocktail.id}",
            **kwargs,
        )

    @classmethod
    def all_view(
        cls,
        cocktails: Sequence[Cocktail],
        ingredients: Sequence[Ingredient] | None = None,
    ) -> FT:
        search = Search(
            Input(
                placeholder="Введите название",
                name="search",
                type="search",
                cls="form-control",
                hx_post="/cocktails/search",
                hx_trigger="input changed delay:500ms, keyup[key=='Enter'], load",
                hx_target="#cocktail-list",
            ),
        )
        header = [search]

        if ingredients:
            ingredient_filter = Select(
                *[
                    Option(ingredient.name, id=ingredient.id, value=ingredient.id)
                    for ingredient in ingredients
                ],
                search="true",
                multiple="true",
                hx_post="/cocktails/filter",
                data_yo_search="true",
                id="ingredient-filter",
                name="filters",
                hx_target="#cocktail-list",
            )
            header.append(ingredient_filter)
            header.append(
                Script(
                    code="""
                    filter = new YoSelect(document.querySelector('#ingredient-filter'), {
                        search: true,
                        searchPlaceholder: 'Найти ингредиент...',
                        noResultsPlaceholder: 'Ингридиентов не найдено',
                        classTag: 'tag-badge',
                    });
                """,
                ),
            )

        add_button = Button(
            NotStr(PLUS_ICON_32),
            data_target="cocktail-modal-add",
            onclick="toggleModal(event)",
            hx_get="/cocktails/add",
            hx_swap="none",
            Class="add",
        )

        rows = [cls.row_view(i) for i in cocktails]
        head = Thead(
            *map(Th, (P("Название"), P("Описание"), P(""), P(""), add_button)),
            cls="bg-purple/10",
        )
        content = Card(
            Table(head, Tbody(*rows, id="cocktail-list"), cls="table"),
            header=Div(*header),
            footer=Div(id="current-cocktail"),
        )

        read_modal = Dialog(
            Card(id="cocktail-modal-read-card"),
            id="cocktail-modal-read",
        )
        edit_modal = Dialog(
            Card(id="cocktail-modal-edit-card"),
            id="cocktail-modal-edit",
        )
        add_modal = Dialog(
            Card(id="cocktail-modal-add-card"),
            id="cocktail-modal-add",
        )

        return Main(
            H1("Рецепты коктейлей"),
            content,
            read_modal,
            edit_modal,
            add_modal,
            id="content",
            cls="container",
            hx_swap="outerHTML",
            # hx_on__before_send="this.replaceChildren();",
            # hx_on__before_swap="console.log(this);",
            hx_target="#content",
        )

    @classmethod
    def get_ingredients_list(
        cls,
        components: list[tuple[Ingredient, int]],
        cocktail_id: int | None,
        form_id: str,
    ) -> list[FT]:
        params = f"cocktail-id={cocktail_id}" if cocktail_id else ""
        return [
            Li(
                f"{ingredient.name} {quantity} {ingredient.unit_measurement}",
                Button(
                    "Удалить",
                    hx_target=f"#{form_id}",
                    hx_include="[name='ingredient'],[name='quantity'],[name='name'],[name='description']",
                    hx_get=f"/cocktails/add/form/?{params}&deleted-id={ingredient.id}",
                    style="width: 150px",
                    Class="delete",
                ),
                Hidden(value=ingredient.id, id=f"ingredient-id-{ingredient.id}"),
                Hidden(value=quantity, id=f"quantity-{ingredient.id}"),
                id=f"component-{ingredient.id}",
            )
            for (ingredient, quantity) in components
        ]

    @classmethod
    def edit_form(
        cls,
        ingredients: Sequence[Ingredient],
        components: list[tuple[Ingredient, int]],
        item_id: int | None = None,
        *,
        is_start_form: bool = False,
    ) -> FT:
        if item_id:
            hx_patch = f"/cocktails/{item_id}"
            hx_post = None
            data_target_suffix = "edit"
            form_id = "edit-form"
            params = f"?cocktail-id={item_id}"
        else:
            hx_patch = None
            hx_post = "/cocktails"
            data_target_suffix = "add"
            form_id = "add-form"
            params = ""

        components_li = cls.get_ingredients_list(components, item_id, form_id)
        label = "Ингредиенты:" if components_li else "Ингредиенты отсутствуют"

        select_options = [
            Option(ingredient.name, id=ingredient.id) for ingredient in ingredients
        ]

        hx_vals = None

        if not is_start_form:
            hx_vals = {
                "ingredients": ",".join(str(i.id) for i, _ in components),
                "quantities": ",".join(str(i) for _, i in components),
            }

        form = Form(
            Label("Название", Input(id="name")),
            Label(
                "Описание",
                Textarea(
                    placeholder="Введите описание ингредиента...",
                    id="description",
                ),
            ),
            Grid(
                Select(
                    *select_options,
                    searchable="true",
                    data_yo_search="true",
                    data_yo_creatable="true",
                    id="ingredient",
                    name="ingredient",
                ),
                Input(
                    id="quantity", name="quantity", value=0, placeholder="Количество"
                ),
                Button(
                    "Добавить",
                    hx_get=f"/cocktails/add/form{params}",
                    hx_include="[name='ingredient'],[name='quantity'],[name='name'],[name='description']",
                    style="width: 150px",
                    target_id=form_id,
                    Class="add",
                ),
                style="grid-template-columns: 3fr 1fr 1fr",
            ),
            Div(
                Div(P(label), Ul(*components_li)),
            ),
            Button(
                "Сохранить",
                autofocus=True,
                data_target=f"cocktail-modal-{data_target_suffix}",
                onclick="toggleModal(event)",
                hx_post=hx_post,
                hx_patch=hx_patch,
                hx_target="#cocktail-list",
                hx_swap="beforeend",
                Class="add",
            ),
            Script(
                code="""
                    new YoSelect(document.querySelector('#ingredient'), {
                        search: true,
                        searchPlaceholder: 'Найти ингридиент...',
                        noResultsPlaceholder: 'Ингридиентов не найдено',
                    });
                """,
            ),
            id=form_id,
            hx_vals=hx_vals,
            hx_on__before_swap="this.replaceChildren();",
        )
        return form

    @classmethod
    def detail_view(cls, cocktail: Cocktail) -> FT:
        components = [
            Li(f"{i.ingredient.name} {i.quantity} {i.ingredient.unit_measurement}")
            for i in cocktail.components
        ]

        label = "Ингредиенты:" if components else "Ингредиенты отсутствуют"

        content = Card(
            Div(
                P(cocktail.description),
                Div(P(label), Ul(*components)),
            ),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="cocktail-modal-read",
                    onclick="toggleModal(event)",
                ),
                H3(cocktail.name, id="cocktail-name-modal"),
            ),
            footer=Div(
                Button(
                    "Закрыть",
                    autofocus=True,
                    data_target="cocktail-modal-read",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 900px",
            id="cocktail-modal-read-card",
        )
        return content

    @classmethod
    def create_view(cls, ingredients: Sequence[Ingredient]) -> FT:
        return Card(
            cls.edit_form(ingredients, [], is_start_form=True),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="cocktail-modal-add",
                    onclick="toggleModal(event)",
                ),
                H3("Добавить коктейль", id="cocktail-name-modal"),
            ),
            footer=Div(
                Button(
                    "Отменить",
                    role="button",
                    cls="secondary",
                    data_target="cocktail-modal-add",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 1000px; max-width: 1000px",
            id="cocktail-modal-add-card",
        )

    @classmethod
    def update_view(cls, cocktail: Cocktail, ingredients: Sequence[Ingredient]) -> FT:
        form = cls.edit_form(
            ingredients=[
                i
                for i in ingredients
                if i.id not in set(i.ingredient.id for i in cocktail.components)
            ],
            components=[(i.ingredient, i.quantity) for i in cocktail.components],
            item_id=cocktail.id,
            is_start_form=False,
        )

        return Card(
            fill_form(form, cocktail),
            header=Div(
                Button(
                    aria_label="Close",
                    rel="prev",
                    data_target="cocktail-modal-edit",
                    onclick="toggleModal(event)",
                ),
                H3(cocktail.name, id="cocktail-name-modal"),
            ),
            footer=Div(
                Button(
                    "Отменить",
                    role="button",
                    cls="secondary",
                    data_target="cocktail-modal-edit",
                    onclick="toggleModal(event)",
                ),
            ),
            hx_swap_oob="true",
            style="width: 1000px; max-width: 1000px",
            id="cocktail-modal-edit-card",
        )

    @classmethod
    def delete_view(cls, item_id: int) -> FT:
        return clear(f"cocktail-{item_id}")
