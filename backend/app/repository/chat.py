from sqlalchemy.orm import Session

from backend.app.model.chat import Chat
from backend.app.model.message import Message
from backend.app.repository.base import BaseRepository


class ChatRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Chat, db)

    def find_by_user_id(self, user_id: int) -> list[Chat]:
        return (
            self.db.query(Chat)
            .filter(Chat.user_id == user_id, Chat.is_deleted.is_(False))
            .order_by(Chat.created_at.desc())
            .all()
        )

    def find_by_chat_id(self, chat_id: str, user_id: int | None = None) -> Chat | None:
        return(self.db.query(Chat).filter(Chat.chat_id == chat_id).filter(Chat.user_id == user_id).first())


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def find_by_chat_id(self, chat_id: str, user_id) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .filter(Message.user_id == user_id)
            .order_by(Message.sequence.asc(), Message.created_at.asc())
            .all()
        )

    def delete_by_chat(self, chat_id: str) -> None:
        (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .delete(synchronize_session=False)
        )

    def next_sequence(self, chat_id: str) -> int:
        last_sequence = (
            self.db.query(Message.sequence)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.sequence.desc())
            .limit(1)
            .scalar()
        )
        return (last_sequence or 0) + 1
