from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.flashcard import DifficultyLevel

class FlashcardBase(BaseModel):
    question: str
    answer: str
    subject: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = DifficultyLevel.MEDIUM

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None

class FlashcardReview(BaseModel):
    is_correct: bool

class FlashcardResponse(FlashcardBase):
    id: int
    user_id: int
    times_reviewed: int
    times_correct: int
    next_reviews: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class FlashcardListResponse(BaseModel):
    flashcards: list[FlashcardResponse]
    total: int