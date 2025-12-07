from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
import json

from ..database import get_db
from ..models.chat_messages import ChatMessage
from ..models.user import User
from ..utils.websocket_manager import manager
from ..utils.jwt import decode_access_token

router = APIRouter(tags=["WebSocket"])

async def get_user_from_token(token: str, db: Session) -> User:
    """Get user from JWT token"""
    payload = decode_access_token(token)
    if not payload:
        return None
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.websocket("/ws/chat/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time chat in study rooms"""
    
    # Authenticate user
    user = await get_user_from_token(token, db)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    # Connect to room
    await manager.connect(websocket, room_id, user.id)
    
    # Notify others that user joined
    await manager.broadcast({
        "type": "user_joined",
        "user_id": user.id,
        "user_name": user.name,
        "timestamp": datetime.utcnow().isoformat()
    }, room_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Save message to database
            chat_message = ChatMessage(
                room_id=room_id,
                user_id=user.id,
                message=message_data.get("message", "")
            )
            db.add(chat_message)
            db.commit()
            db.refresh(chat_message)
            
            # Broadcast message to all users in room
            await manager.broadcast({
                "type": "message",
                "id": chat_message.id,
                "user_id": user.id,
                "user_name": user.name,
                "message": chat_message.message,
                "timestamp": chat_message.timestamp.isoformat()
            }, room_id)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        
        # Notify others that user left
        await manager.broadcast({
            "type": "user_left",
            "user_id": user.id,
            "user_name": user.name,
            "timestamp": datetime.utcnow().isoformat()
        }, room_id)
    
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, room_id)

@router.get("/api/chat/history/{room_id}")
async def get_chat_history(
    room_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a room"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.room_id == room_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
    
    messages.reverse()  # Return in chronological order
    
    return {
        "room_id": room_id,
        "messages": [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "user_name": msg.user.name,
                "message": msg.message,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    }

@router.get("/api/chat/rooms")
async def get_available_rooms():
    """Get list of available study rooms"""
    # In a real app, you might want to store rooms in database
    # For now, return some default rooms
    rooms = [
        {"id": "math-101", "name": "Math 101 Study Group", "subject": "Mathematics"},
        {"id": "physics-201", "name": "Physics 201", "subject": "Physics"},
        {"id": "cs-fundamentals", "name": "Computer Science Fundamentals", "subject": "CS"},
        {"id": "general", "name": "General Study Hall", "subject": "General"}
    ]
    
    # Add active user counts
    for room in rooms:
        room["active_users"] = len(manager.get_room_users(room["id"]))
    
    return {"rooms": rooms}