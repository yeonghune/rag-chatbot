from typing import List

from backend.app.repository.base import transactional
from backend.app.repository.chat import ChatRepository, MessageRepository
from backend.app.schemas.chat import ChatCreate, ChatOut, MessageCreate, MessageOut


class ChatService:
    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository) -> None:
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    def list_chats(self, user_id: int) -> List[ChatOut]:
        return [ChatOut.from_model(chat) for chat in self.chat_repo.find_by_user_id(user_id)]

    @transactional
    def create_chat(self, user_id: int, request: ChatCreate) -> ChatOut:
        return ChatOut.from_model(self.chat_repo.add(request.to_model(user_id)))

    def get_chat(self, chat_id: str, user_id: int) -> ChatOut:
        return ChatOut.from_model(self.chat_repo.find_by_chat_id(chat_id, user_id))

    @transactional
    def delete_chat(self, chat_id: str, user_id: int) -> None:
        chat = self.chat_repo.find_by_chat_id(chat_id, user_id)
        if chat is None:
            return

        chat.is_deleted = True
        self.chat_repo.update(chat)

    def list_messages(self, chat_id: str, user_id: int) -> List[MessageOut]:
        return [MessageOut.from_model(message) for message in self.message_repo.find_by_chat_id(chat_id, user_id)]

    @transactional
    def send_message(self, chat_id: str, user_id: int, payload: MessageCreate) -> MessageOut:
        print(payload.content)
        return True
