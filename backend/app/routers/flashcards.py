from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta, timezone

from ..database import get_db
from ..models.user import User
from ..models.flashcard import Flashcard
from ..schemas.flashcard import (
    FlashcardCreate, FlashcardUpdate, FlashcardResponse, 
    FlashcardListResponse, FlashcardReview
)
from ..routers.auth import get_current_user

router = APIRouter(prefix="/api/flashcards", tags=["Flashcards"])

@router.post("/", response_model=FlashcardResponse, status_code=status.HTTP_201_CREATED)
async def create_flashcard(
    flashcard: FlashcardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    db_flashcard = Flashcard(
        user_id = current_user.id,
        question = flashcard.question, 
        answer = flashcard.answer,
        subject = flashcard.subject,
        difficulty = flashcard.difficulty
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

@router.get("/", response_model=FlashcardListResponse)
async def get_flashcards(
    subject: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    "get all flashcards"
    query = db.query(Flashcard).filter(Flashcard.user_id == current_user.id)
    if subject:
        query = query.filter(Flashcard.subject == subject)

    flashcards = query.order_by(Flashcard.created_at.desc()).all()

    return {
        "flashcards": flashcards,
        "total": len(flashcards)
    }

@router.get("/due", response_model=FlashcardListResponse)
async def get_due_flashcards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    "get flashcards due for review"
    now = datetime.now(timezone.utc)
    flashcards = db.query(Flashcard).filter(
        Flashcard.user_id == current_user.id,
        (Flashcard.next_review <= now) | (Flashcard.next_review.is_(None))
    ).limit(20).all()

    return {
        "flashcards": flashcards,
        "total": len(flashcards)
    }

@router.get("/{flashcard_id}", response_model=FlashcardResponse)
async def get_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    "get a flas"
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard

@router.put("/{flashcard_id}", response_model=FlashcardResponse)
async def update_flashcard(
    flashcard_id: int,
    flashcard_update: FlashcardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    update_data = flashcard_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flashcard, field, value)
    
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.delete("/{flashcard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    db.delete(flashcard)
    db.commit()
    return None

@router.post("/{flashcard_id}/review", response_model=FlashcardResponse)
async def review_flashcard(
    flashcard_id: int,
    review: FlashcardReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    """record a review"""
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    #update statistics
    flashcard.times_reviewed += 1
    if review.is_correct:
        flashcard.times_correct += 1
    #calculate next review date
    if review.is_correct:
        #increase interval on diff
        if flashcard.difficulty.value == "easy":
            days = 7
        elif flashcard.difficulty.value == "medium":
            days = 3
        else:
            days = 1
        #multipler on success rate
        success_rate = flashcard.times_correct / flashcard.times_reviewed
        if success_rate > 0.8:
            days *= 2
        flashcard.next_review = datetime.now(timezone.utc) + timedelta(days=days)
    else: 
        flashcard.next_review = datetime.now(timezone.utc) + timedelta(hours=4)
    
    db.commit()
    db.refresh(flashcard)
    return flashcard