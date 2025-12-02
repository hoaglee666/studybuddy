from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageCreate(BaseModel):
    room_id: str
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    message: str
    timestamp: datetime
    user_name: str #added from user rela

    class Config:
        from_attributes = True

class AIMessageRequest(BaseModel):
    message: str
    context: Optional[str] = None #additional context for ai

class AIMessageResponse(BaseModel):
    message: str
    model: str

class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[str] = 150

class QuizGenerateRequest(BaseModel):
    content: str
    num_questions: Optional[int] = 5