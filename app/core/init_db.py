from sqlmodel import Session, select

from app.models import Ingredient

INGREDIENTS = [
    {
        "name": "Водка",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Пряный ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Виски",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Лондонский сухой джин",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Белый ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Коньяк",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Выдержанный ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Темный ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {
        "name": "Золотой ром",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Крепкая часть",
    },
    {"name": "Абсент", "unit_measurement": "мл", "abv": "Крепкий", "type_": "Ликёр"},
    {
        "name": "Самбука классическая",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Ликёр",
    },
    {"name": "Трипл сек", "unit_measurement": "мл", "abv": "Крепкий", "type_": "Ликёр"},
    {
        "name": "Кофейный ликер",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Ликёр",
    },
    {
        "name": "Ликер мараскино",
        "unit_measurement": "мл",
        "abv": "Крепкий",
        "type_": "Ликёр",
    },
    {
        "name": "Айриш крим",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Ликёр",
    },
    {
        "name": "Красный вермут",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Вермут",
    },
    {
        "name": "Сухой вермут",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Вермут",
    },
    {
        "name": "Белый вермут",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Вермут",
    },
    {
        "name": "Розовый вермут",
        "unit_measurement": "мл",
        "abv": "Слабоалкогольные",
        "type_": "Вермут",
    },
    {"name": "Мёд", "unit_measurement": "мл", "abv": None, "type_": "Другое"},
    {
        "name": "Содовая",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Спрайт",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Кола",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Тоник",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Лимонный сок",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Лаймовый сок",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Апельсиновый сок",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Яблочный сок",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Безалкогольная часть",
    },
    {
        "name": "Сахарный сироп",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Сироп",
    },
    {
        "name": "Медовый сироп",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Сироп",
    },
    {
        "name": "Гренадин",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Сироп",
    },
    {
        "name": "Сироп маракуйи",
        "unit_measurement": "мл",
        "abv": "Безалкогольные",
        "type_": "Сироп",
    },
]


def init_db(session: Session) -> None:
    current_ingredients = set(session.exec(select(Ingredient.name)))

    for item in INGREDIENTS:
        ingredient = Ingredient.model_validate(item)

        if ingredient.name not in current_ingredients:
            session.add(ingredient)

    session.commit()
