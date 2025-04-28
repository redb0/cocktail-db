from sqlmodel import Field, Relationship

from app.models.base import Base
from app.models.cocktail import Cocktail
from app.models.ingredient import Ingredient


class ComponentBase(Base):
    quantity: int = Field(
        ge=0,
        description="Количество",
    )
    ingredient_id: int = Field(
        foreign_key="ingredient.id",
    )
    cocktail_id: int = Field(
        foreign_key="cocktail.id",
        ondelete="CASCADE",
    )


class Component(ComponentBase, table=True):
    ingredient: Ingredient = Relationship()
    cocktail: Cocktail = Relationship()


# class ComponentCreate(ComponentBase):
#     pass


# class ComponentPublic(ComponentBase):
#     id: int
