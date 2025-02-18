from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    conversation_id: int
    text: str

class MessageResponse(BaseModel):
    id: int
    sender: str
    text: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
