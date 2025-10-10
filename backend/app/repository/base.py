import functools
from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def add(self, obj: T) -> T:
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.db.merge(obj)
        return obj

    def get(self, id_: int) -> T | None:
        return self.db.get(self.model, id_)

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def delete(self, obj: T) -> None:
        self.db.delete(obj)

    def merge(self, obj: T) -> T:
        merged = self.db.merge(obj)
        self.db.flush()
        return merged


def transactional(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        repository = None

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, BaseRepository):
                repository = attr
                break

        if repository is None:
            raise AttributeError(f'Cannot find repository in service class: {self.__class__.__name__}')

        db = getattr(repository, 'db', None)
        if db is None or not isinstance(db, Session):
            raise AttributeError('Repository instance does not expose a valid Session')

        try:
            result = func(self, *args, **kwargs)
            db.commit()
            return result
        except Exception as exc:
            db.rollback()
            raise exc

    return wrapper
