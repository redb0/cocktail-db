from app.models.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from app.services.base import BaseService


class IngredientService(BaseService[Ingredient, IngredientCreate, IngredientUpdate]):
    def __init__(self, session):
        super().__init__(Ingredient, session)
