from backend.app.model.user import User
from backend.app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(User, db)

    def find_by_username(self, name: str) -> User:
        return self.db.query(User).filter(User.name == name).first()

    def activate(self, obj: User) -> User:
        obj.is_active = True
        self.db.merge(obj)
        return obj

    def deactivate(self, obj: User) -> User:
        obj.is_active = False
        self.db.merge(obj)
        return obj
