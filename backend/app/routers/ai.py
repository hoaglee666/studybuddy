from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.note import Note
from ..models.flashcard import Flashcard
from ..schemas.chat import (
    AIMessageRequest, AIMessageResponse,
    SummarizeRequest, QuizGenerateRequest
)
from ..routers.auth import get_current_user
from ..services.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI Features"])

@router.post("/chat", response_model=AIMessageResponse)
async def chat_with_assistant(
    request: AIMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    try:
        context = request.context
        if not context:
            recent_notes = db.query(Note).filter(
                Note.user_id == current_user.id
            ).order_by(Note.updated_at.disc()).limit(3).all()

            if recent_notes:
                context = "\n\n".join([f"Title: {n.title}\n{n.content}" for n in recent_notes])
        
        response = await ai_service.chat_with_assistant(request.message, context)
        
        return {
            "message": response,
            "model": "gpt-4"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.post("/summarize")
async def summarize_text(
    request: SummarizeRequest,
    current_user: User = Depends(get_current_user)
): 
    try:
        summary = await ai_service.summarize_text(request.text, request.max_length)
        return {
            "summary": summary,
            "original_length": len(request.text),
            "summary_length": len(summary)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.post("/generate-quiz")
async def generate_quiz(
    request: QuizGenerateRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        quiz = await ai_service.generate_quiz(request.context, request.num_questions)
        return {
            "questions": quiz,
            "total": len(quiz)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
    
@router.post("/generate-flashcards")
async def generate_flashcards_from_content(
    note_id: int,
    num_cards: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    #get note
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    try:
        #generate flashcards using ai
        flashcards_data = await ai_service.generate_flashcards(note.content, num_cards)
        #save gnerated flas
        created_flashcards = []
        for card_data in flashcards_data:
            flashcard = Flashcard(
                user_id=current_user.id,
                question=card_data.get('question', ''),
                answer=card_data.get('answer', ''),
                subject=note.subject,
                difficulty=card_data.get('difficulty', 'medium')
            )
            db.aad(flashcard)
            created_flashcards.append(flashcard)
        db.commit()

        return {
            "message": f"Generated {len(created_flashcards)} flashcards from note.",
            "flashcards": [
                {
                    "id": fc.id,
                    "question": fc.question,
                    "answer": fc.answer,
                    "difficulty": fc.difficulty
                } 
                for fc in created_flashcards
            ]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
    
@router.post("/smart-search")
async def smart_search(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    """natural search"""
    #get all note
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    if not notes:
        return {"results": [], "message": "No notes found"}
    #prepare note content
    notes_content = [f"Note ID {n.id}: {n.title}\n{n.content}" for n in notes]
    
    try:
        result = await ai_service.smart_search(query, notes_content)
        return {
            "query": query,
            "result": result,
            "notes_searched": len(notes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")