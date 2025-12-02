from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from ..database import get_db
from ..models.user import User
from ..models.note import Note
from ..models.flashcard import Flashcard
from ..models.study_sessions import StudySession
from ..routers.auth import get_current_user

router_analytics = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router_analytics.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
): 
    #total counts
    total_notes = db.query(func.count(Note.id)).filter(Note.user_id == current_user.id).scalar()
    total_flashcards = db.query(func.count(Flashcard.id)).filter(Flashcard.user_id == current_user.id).scalar()
    total_sessions = db.query(func.count(StudySession.id)).filter(StudySession.user_id == current_user.id).scalar()
    #study time last 7
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    study_time_week = db.query(func.sum(StudySession.duration_minutes)).filter(
        StudySession.user_id == current_user.id,
        StudySession.created_at >= seven_days_ago
    ).scalar() or 0
    #study time last 30
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    study_time_month = db.query(func.sum(StudySession.duration_minutes)).filter(
        StudySession.user_id == current_user.id,
        StudySession.created_at >= thirty_days_ago
    ).scalar() or 0
    #flashcards statis
    flashcard_stats = db.query(
        func.sum(Flashcard.times_reviewed).label("total_reviews"),
        func.sum(Flashcard.times_correct).label("total_correct")
    ).filter(Flashcard.user_id == current_user.id).first()

    accuracy = 0
    if flashcard_stats.total_reviews and flashcard_stats.total_reviews > 0:
        accuracy = (flashcard_stats.total_correct / flashcard_stats.total_reviews) * 100
    
    #recent activity 
    daily_activity = []
    for i in range(7):
        date = datetime.now(timezone.utc) - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        duration = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.user_id == current_user.id,
            StudySession.created_at >= date_start,
            StudySession.created_at < date_end
        ).scalar() or 0
        daily_activity.append({
            "date": date_start.strftime("%Y-%m-%d"),
            "study_time_minutes": duration
        })
    daily_activity.reverse()
    #study by subj
    subject_breakdown = db.query(
        Note.subject,
        func.count(Note.id).label("note_count"),
    ).filter(
        Note.user_id == current_user.id,
        Note.subject.isnot(None)
    ).group_by(Note.subject).all()

    return {
        "totals": {
            "notes": total_notes,
            "flashcards": total_flashcards,
            "study_sessions": total_sessions,
            "study_time_week": study_time_week,
            "study_time_month": study_time_month,
        },
        "flashcard_accuracy": round(accuracy, 2),
        "daily_activity": daily_activity,
        "subject_breakdown": [
            {"subject": subject, "note_count": note_count} 
            for subject, note_count in subject_breakdown
        ],
    }