from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlmodel import Session

from app.api.main import app_router
from app.core.config import settings
from app.core.db import engine
from app.core.init_db import init_db


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Дополнительная логика запуска и завершения работы."""
    from app.models import Base

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        init_db(session)

    yield


def get_application() -> FastAPI:
    """Создать приложение FastAPI."""
    app_ = FastAPI(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=lifespan,
    )
    app_.include_router(app_router)

    return app_


app = get_application()


def main() -> None:
    """Точка входа."""
    uvicorn.run(app)


if __name__ == "__main__":
    main()
