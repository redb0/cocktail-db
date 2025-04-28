from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlmodel import Session, SQLModel, col, delete, select

from app.models.base import Base

_ModelType = TypeVar("_ModelType", bound=Base)
_CreateModelType = TypeVar("_CreateModelType", bound=SQLModel)
_UpdateModelType = TypeVar("_UpdateModelType", bound=SQLModel)


class BaseService(Generic[_ModelType, _CreateModelType, _UpdateModelType]):
    def __init__(self, model: type[_ModelType], session: Session) -> None:
        self.model = model
        self.session = session

    def get(self, item_id: int) -> _ModelType | None:
        return self.session.get(self.model, item_id)

    def get_all(self) -> Sequence[_ModelType]:
        query = select(self.model)
        return self.session.exec(query).all()

    def create(self, data: _CreateModelType) -> _ModelType:
        if isinstance(data, dict):
            data = self.model.model_validate(data)
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        # NOTE: Для преобразования типа
        return self.model.model_validate(data)

    def update(self, item_id: int, data: _UpdateModelType) -> _ModelType:
        item = self.get(item_id)
        if item is None:
            msg = "Доделать"
            raise ValueError(msg)

        item.sqlmodel_update(data.model_dump(exclude_unset=True))
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item_id: int) -> None:
        query = delete(self.model).where(col(self.model.id) == item_id)
        self.session.exec(query)  # type: ignore[call-overload]
        self.session.commit()
