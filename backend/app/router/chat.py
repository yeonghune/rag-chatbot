from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from backend.app.core.deps import get_current_user, get_chat_service
from backend.app.model.user import User
from backend.app.schemas.chat import ChatCreate, ChatOut, MessageCreate, MessageOut
from backend.app.service.chat import ChatService

router = APIRouter(tags=["Chat API"], prefix="/api/chats")


@cbv(router)
class ChatRouter:
    def __init__(self, chat_service: ChatService = Depends(get_chat_service)) -> None:
        self.chat_service = chat_service

    @router.get("/", response_model=list[ChatOut])
    def list_chats(self, current_user: User = Depends(get_current_user)) -> list[ChatOut]:
        chats = self.chat_service.list_chats(current_user.user_id)
        return list(chats) if chats is not None else []

    @router.post("/", response_model=ChatOut)
    def create_chat(
        self,
        payload: ChatCreate,
        current_user: User = Depends(get_current_user),
    ) -> ChatOut:
        return self.chat_service.create_chat(current_user.user_id, payload)

    @router.get("/{chat_id}", response_model=ChatOut)
    def get_chat(self, chat_id: str, current_user: User = Depends(get_current_user)) -> ChatOut:
        return self.chat_service.get_chat(chat_id, current_user.user_id)

    @router.delete("/{chat_id}")
    def delete_chat(self, chat_id: str, current_user: User = Depends(get_current_user)) -> None:
        self.chat_service.delete_chat(chat_id, current_user.user_id)

    @router.get("/{chat_id}/messages", response_model=list[MessageOut])
    def list_messages(self, chat_id: str, current_user: User = Depends(get_current_user)) -> list[MessageOut]:
        messages = self.chat_service.list_messages(chat_id, current_user.user_id)
        return list(messages) if messages is not None else []

    @router.post("/{chat_id}/messages")
    def send_message(
        self,
        chat_id: str,
        payload: MessageCreate,
        current_user: User = Depends(get_current_user),
    ):
        return self.chat_service.send_message(chat_id, current_user.user_id, payload)
