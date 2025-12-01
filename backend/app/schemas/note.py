from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None
    subject: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    subject: Optional[str] = None
    image_url: Optional[str] = None

class NoteResponse(NoteBase):
    id: int
    user_id: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config: 
        from_attributes = True

class NoteListResponse(BaseModel):
    notes: list[NoteResponse]
    total: int
    page: int
    page_size: int
    total_pages: int