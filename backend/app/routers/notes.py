from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
import math

from ..database import get_db
from ..models.user import User
from ..models.note import Note
from ..schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteListResponse
from ..routers.auth import get_current_user
from ..services.file_service import file_service

router = APIRouter(prefix="/api/notes", tags=["Notes"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_note = Note(
        user_id=current_user.id,
        title=note.title,
        content=note.content,
        tags=note.tags,
        subject=note.subject
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=NoteListResponse)
async def get_notes(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    subject: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|updated_at|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """get all notes for curr user with pagination, search, filtering, and sorting"""
    query = db.query(Note).filter(Note.user_id == current_user.id)

    #search
    if search:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{search}"),
                Note.content.ilike(f"%{search}"),
                Note.tags.ilike(f"%{search}")
            )
        )
    #subject
    if subject: 
        query = query.filter(Note.subject == subject)
    #total count
    total = query.count()
    #sorting
    if sort_order == "desc":
        query = query.order_by(getattr(Note, sort_by).desc())
    else: 
        query = query.order_by(getattr(Note, sort_by).asc())
    #pagination
    offset = (page - 1) * page_size
    notes = query.offset(offset).limit(page_size).all()
    total_pages = math.ceil(total / page_size)

    return {
        "notes": notes,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    """get a note"""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    #update fiedl
    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    #delete iamge too
    if note.image_url:
        file_service.delete_file(note.image_url)

    db.delete(note)
    db.commit()
    return None

@router.post("/{note_id}/upload-image")
async def upload_note_image(
    note_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    #delete old image
    if note.image_url:
        file_service.delete_file(note.image_url)
    #save new
    file_path = await file_service.save_upload_file(file, current_user.id)
    note.image_url = file_path
    db.commit()
    db.refresh(note)

    return {
        "message": "Image uploaded successfully",
        "image_url": file_service.get_file_url(file_path)
    }

@router.get("/subjects/list")
async def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    subjects = db.query(Note.subject).filter(
        Note.user_id == current_user.id,
        Note.subject.isnot(None)
    ).distinct().all()

    return {"subjects": [s[0] for s in subjects if s[0]]}