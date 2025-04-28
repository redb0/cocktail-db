import sqlalchemy as sa
from sqlmodel import Field, SQLModel

from app.models.base import Base
from app.models.enums import IngredientType, TypeABV, UnitMeasurement


class IngredientBase(Base):
    name: str = Field(
        min_length=3,
        max_length=512,
        description="Наименование ингридиента",
    )
    description: str | None = Field(
        default=None,
        max_length=512,
        description="Описание",
    )
    unit_measurement: UnitMeasurement = Field(
        default=UnitMeasurement.MILLILITER,
        description="Единица измерения",
    )
    abv: TypeABV | None = Field(
        default=None,
        description="Крепость",
    )
    type_: IngredientType = Field(
        default=IngredientType.OTHER,
        description="Тип",
    )

    icon: bytes | None = Field(  # type: ignore[call-overload]
        default=None,
        sa_type=sa.LargeBinary(),
        nullable=True,
        description="Иконка",
    )


class Ingredient(IngredientBase, table=True):
    pass


class IngredientCreate(IngredientBase):
    pass


# class IngredientPublic(IngredientBase):
#     id: int


class IngredientUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    unit_measurement: UnitMeasurement | None = None
    abv: TypeABV | None = None
    type_: IngredientType | None = None
