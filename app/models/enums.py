from enum import StrEnum


class UnitMeasurement(StrEnum):
    MILLILITER = "мл"
    GRAM = "гр"
    PIECE = "шт"


class TypeABV(StrEnum):
    FREE = "Безалкогольные"
    LOW = "Слабоалкогольные"
    STRONG = "Крепкий"


class IngredientType(StrEnum):
    STRONG_PART = "Крепкая часть"
    NON_ALCOHOLIC_PART = "Безалкогольная часть"
    VERMOUTH = "Вермут"
    LIQUOR = "Ликёр"
    BITTER = "Биттер"
    SYRUP = "Сироп"
    OTHER = "Другое"
    FRUIT = "Фрукт"
    VEGETABLE = "Овощ"
    BERRY = "Ягода"
