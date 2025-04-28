from collections.abc import Sequence

from sqlalchemy import func
from sqlmodel import col, select

from app.models import Component, Ingredient
from app.models.cocktail import Cocktail, CocktailCreate, CocktailUpdate
from app.models.forms import FiltersFrom
from app.services.base import BaseService


class CocktailService(BaseService[Cocktail, CocktailCreate, CocktailUpdate]):
    def __init__(self, session):
        super().__init__(Cocktail, session)

    def filter_all(self, filters: FiltersFrom) -> Sequence[Cocktail]:
        if filters.filters:
            query = (
                select(self.model)
                .join(Component, col(self.model.id) == col(Component.cocktail_id))
                .join(Ingredient, col(Component.ingredient_id) == col(Ingredient.id))
                .where(col(Component.ingredient_id).in_(filters.filters))
                .group_by(col(self.model.id))
                .having(
                    func.count(col(Ingredient.id).distinct()) == len(filters.filters)
                )
            )
            cocktails = self.session.exec(query).all()
        else:
            cocktails = self.get_all()
        return cocktails

    def search(self, value: str | None) -> Sequence[Cocktail]:
        if value:
            query = select(Cocktail).where(col(Cocktail.name).ilike(f"%{value}%"))
        else:
            query = select(Cocktail)
        return self.session.exec(query).all()

    def create(self, data: CocktailCreate) -> Cocktail:
        new_cocktail = Cocktail.model_validate(
            data.model_dump(include={"name", "description"}),
        )
        new_cocktail.components = [
            Component(quantity=int(quantity), ingredient_id=int(ingredient_id))
            for ingredient_id, quantity in data.components.items()
        ]

        self.session.add(new_cocktail)
        self.session.commit()
        self.session.refresh(new_cocktail)

        return new_cocktail

    def update(self, item_id: int, data: CocktailUpdate) -> Cocktail:
        cocktail = self.get(item_id)
        if cocktail is None:
            msg = "Доделать"
            raise ValueError(msg)

        cocktail.sqlmodel_update(
            data.model_dump(include={"name", "description"}, exclude_unset=True),
        )

        components = data.components

        deleted = []
        updated = []
        for component in cocktail.components:
            if component.ingredient_id not in components:
                deleted.append(component)
            else:
                new_quantity = components[component.ingredient_id]
                if new_quantity != component.quantity:
                    component.quantity = new_quantity
                    updated.append(component)
                components.pop(component.ingredient_id)

        for ingredient_id, quantity in components.items():
            self.session.add(
                Component(
                    quantity=quantity,
                    ingredient_id=ingredient_id,
                    cocktail_id=cocktail.id,
                )
            )

        self.session.add(cocktail)

        if updated:
            self.session.add_all(updated)

        for item in deleted:
            self.session.delete(item)

        self.session.commit()
        self.session.refresh(cocktail)

        return cocktail
