from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from backend.app.model.chat import Chat
from backend.app.model.message import Message


class ChatCreate(BaseModel):
    title: str = Field(max_length=30)

    def to_model(self, user_id: int) -> Chat:
        return Chat(
            user_id=user_id,
            title=self.title,
        )


class ChatOut(BaseModel):
    chat_id: str = Field(alias="chatId")
    title: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_model(cls, model: Chat):
        return cls.model_validate(
            {
                "chatId": model.chat_id,
                "title": model.title,
                "createdAt": model.created_at,
                "updatedAt": model.updated_at,
            },
            from_attributes=True,
        )


class MessageCreate(BaseModel):
    content: str

    def to_model(self, chat_id: str, user_id: int, sequence: int, role: str) -> Message:
        return Message(
            chat_id=chat_id,
            user_id=user_id,
            sequence=sequence,
            role=role,
            content=self.content,
        )


class MessageOut(BaseModel):
    message_id: str = Field(alias="messageId")
    chat_id: str = Field(alias="chatId")
    user_id: int = Field(alias="userId")
    sequence: int
    role: str
    content: str
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_model(cls, model: Message):
        return cls.model_validate(
            {
                "messageId": model.message_id,
                "chatId": model.chat_id,
                "userId": model.user_id,
                "sequence": model.sequence,
                "role": model.role,
                "content": model.content,
                "createdAt": model.created_at,
            },
            from_attributes=True,
        )
