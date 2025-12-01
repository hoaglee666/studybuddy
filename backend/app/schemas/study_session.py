from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudySessionCreate(BaseModel):
    duration_minutes: int
    notes_reviewed: Optional[int] = 0
    flashcards_practiced: Optional[int] = 0
    subject: Optional[str] = None
    session_type: Optional[str] = None

class StudySessionResponse(StudySessionCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class StudySessionListResponse(BaseModel):
    sessions: list[StudySessionResponse]
    total: int
