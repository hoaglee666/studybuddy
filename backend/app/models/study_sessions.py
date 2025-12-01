from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    duration_minutes = Column(Integer, nullable=False)  # Duration in minutes
    notes_reviewed = Column(Integer, default=0)
    flashcards_practiced = Column(Integer, default=0)
    subject = Column(String(100), nullable=True)
    session_type = Column(String(50), nullable=True)  # reading, quiz, practice
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #relationships
    user = relationship("User", back_populates="study_sessions")