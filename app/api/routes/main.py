from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fasthtml.common import (
    AX,
    H1,
    Body,
    Button,
    Div,
    Head,
    Header,
    Hgroup,
    Html,
    Li,
    Link,
    Main,
    Meta,
    Nav,
    NotStr,
    P,
    Script,
    ScriptX,
    StyleX,
    Title,
    Ul,
    def_hdrs,
    to_xml,
)

from app.api.const import THEME_ICON_32

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def default():
    path = Path(__file__).parent.parent.parent
    content = Html(
        Head(
            *def_hdrs(),
            Meta(content="light dark", name="color-scheme"),
            Title("Рецепты коктейлей"),
            Script(
                src="https://unpkg.com/htmx.org@2.0.4",
                integrity="sha384-HGfztofotfshcF7+8n44JQL2oJmowVChPTg48S+jvZoztPfvwD79OC/LTtG6dMp+",
                crossorigin="anonymous",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/gh/Yohn/PicoCSS@2.2.10/css/pico.min.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/theme-toggles@4.10.1/css/classic.min.css",
            ),
            Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css",
            ),
            StyleX(path / "static/css/my_css.css"),
            StyleX(path / "static/css/yoSelect.css"),
            ScriptX(path / "static/js/yoSelect.js"),
        ),
        Body(
            Header(
                Nav(
                    Ul(
                        Hgroup(
                            Div(
                                H1("База коктейлей"),
                                P("Простая база домашних коктейлей"),
                            ),
                        ),
                    ),
                    Ul(
                        Li(
                            AX(
                                "Коктейли",
                                "cocktails",
                                "content",
                                hx_swap="outerHTML",
                            ),
                            id="menu-1",
                        ),
                        Li(
                            AX(
                                "Ингридиенты",
                                "ingredients",
                                "content",
                                hx_swap="outerHTML",
                            ),
                            id="menu-2",
                        ),
                        Li(
                            Button(
                                Div(
                                    NotStr(THEME_ICON_32),
                                    Class="theme-toggle",
                                    id="theme-toggle",
                                ),
                                Class="contrast",
                                type="button",
                                title="Toggle theme",
                                aria_label="Toggle theme",
                                data_theme_switcher="light",
                            ),
                        ),
                    ),
                ),
                cls="container",
            ),
            Main(
                id="content",
                cls="container",
                hx_get="/cocktails",
                hx_trigger="load",
                hx_swap="outerHTML",
            ),
            ScriptX(path / "static/js/minimal-theme-switcher.js"),
            ScriptX(path / "static/js/modal.js"),
        ),
    )
    return to_xml(content)
