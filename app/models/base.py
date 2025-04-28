import inflection
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class Base(SQLModel):
    """Базовый класс моделей."""

    model_config = SQLModelConfig(
        populate_by_name=True,
        validate_assignment=True,
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        nullable=False,
    )

    # NOTE: Известная проблема типизации __tablename__ https://github.com/tiangolo/sqlmodel/issues/159
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:  # type: ignore[override]
        """Имя таблицы в формате snake_case."""
        return inflection.underscore(cls.__name__)
