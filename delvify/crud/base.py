from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from delvify import models

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self._db = db
        self._model = model

    def get(self, id: Any) -> Optional[ModelType]:
        return self._db.query(self._model).filter(self._model.id == id).first()

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self._db.query(self._model).offset(skip).limit(limit).all()

    def create(self, *, form: CreateSchemaType) -> ModelType:
        form_data = jsonable_encoder(form)
        db_obj = self._model(**form_data)  # type: ignore
        self._db.add(db_obj)
        self._db.commit()
        self._db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: ModelType, form: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(form, dict):
            update_data = form
        else:
            update_data = form.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self._db.add(db_obj)
        self._db.commit()
        self._db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: int) -> ModelType:
        obj = self._db.query(self._model).get(id)
        self._db.delete(obj)
        self._db.commit()
        return obj  # type: ignore
