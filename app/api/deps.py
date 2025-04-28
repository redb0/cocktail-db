from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine
from app.services import CocktailService, IngredientService


def _get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(_get_db)]


def _get_ingredient_service(session: SessionDep) -> IngredientService:
    return IngredientService(session)


IngredientServiceDep = Annotated[IngredientService, Depends(_get_ingredient_service)]


def _get_cocktail_service(session: SessionDep) -> CocktailService:
    return CocktailService(session)


CocktailServiceDep = Annotated[CocktailService, Depends(_get_cocktail_service)]
