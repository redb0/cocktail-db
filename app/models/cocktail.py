from typing import TYPE_CHECKING, Self

import sqlalchemy as sa
from pydantic import computed_field, field_validator, model_validator
from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.component import Component


class CocktailBase(Base):
    name: str = Field(
        min_length=3,
        max_length=512,
        description="Наименование коктейля",
    )
    description: str | None = Field(
        min_length=3,
        max_length=1024,
        description="Описание",
    )
    icon: bytes | None = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=sa.LargeBinary(),
        nullable=True,
        description="Иконка",
    )


class Cocktail(CocktailBase, table=True):
    components: list["Component"] = Relationship(back_populates="cocktail")


class CocktailCreate(CocktailBase):
    ingredients: list[int]
    quantities: list[int]

    @computed_field  # type: ignore[misc]
    @property
    def components(self) -> dict[int, int]:
        return dict(zip(self.ingredients, self.quantities, strict=True))

    @field_validator("ingredients", "quantities", mode="before")
    @classmethod
    def _convert_str_to_list(cls, value: str | list[str] | list[int]) -> list[int]:
        if isinstance(value, str):
            return [int(i) for i in value.split(",")]
        # NOTE: FastAPI сам преобразует значение в список из 1 строки
        if len(value) == 1 and isinstance(value[0], str):
            return [int(i) for i in value[0].split(",")]
        msg = "Неверный формат передачи компонент"
        raise ValueError(msg)

    @model_validator(mode="after")
    def _check_components(self) -> Self:
        if not self.ingredients or not self.quantities:
            msg = "Коктейль должен содержать хотя бы 1 ингредиент"
            raise ValueError(msg)

        if len(self.ingredients) != len(self.quantities):
            msg = "Ошибка сопоставления ингредиентов"
            raise ValueError(msg)

        return self


# class CocktailPublic(CocktailBase):
#     id: int


class CocktailUpdate(CocktailCreate):
    pass
