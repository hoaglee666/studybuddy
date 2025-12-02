from fastapi import APIRouter, Depends, status
from ..schemas.study_session import StudySessionCreate, StudySessionListResponse, StudySessionResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.study_sessions import StudySession
from ..routers.auth import get_current_user
router_sessions = APIRouter(prefix="/api/study-sessions", tags=["Study Sessions"])

@router_sessions.post("/", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
async def create_study_sessions(
    session: StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    """log a sess"""
    db_session = StudySession(
        user_id = current_user.id,
        duration_minutes = session.duration_minutes,
        notes_reviewed = session.notes_reviewed,
        flashcards_practiced = session.flashcards_practiced,
        subject = session.subject,
        session_type = session.session_type
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router_sessions.get("/", response_model=StudySessionListResponse)
async def get_study_sessions(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """get recent study sess"""
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).order_by(StudySession.created_at.desc()).limit(limit).all()

    return {
        "sessions": sessions,
        "total": len(sessions)
    }