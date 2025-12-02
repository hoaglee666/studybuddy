from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import json

from ..database import get_db
from ..models.chat_messages import ChatMessage
from ..models.user import User
from ..utils.websocket_manager import manager
from ..utils.jwt import decode_access_token

router = APIRouter(tags=["WebSocket"])

async def get_user_from_token(
    token: str, db: Session
) -> User:
    """get usr from jwt"""
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
    """websocket endpoint for chat room"""
    #authe user
    user =await get_user_from_token(token, db)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return 
    #connect 
    await manager.connect(websocket, room_id, user.id)
    #notify other when join
    await manager.broadcast({
        "type": "user_joined",
        "user_id": user.id,
        "username": user.username,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }, room_id)
    try: 
        while True:
            #receive message form clien
            data = await websocket.receive_text()
            message_data = json.loads(data)
            #save message to db
            chat_message = ChatMessage(
                room_id=room_id,
                user_id=user.id,
                message=message_data.get("message", "")
            )
            db.add(chat_message)
            db.commit()
            db.refresh(chat_message)
            #broadcas mess to all users in rom
            await manager.broadcast({
                "type": "message",
                "id": chat_message.id,
                "user_id": user.id,
                "username": user.username,
                "message": chat_message.message,
                "timestamp": chat_message.created_at.isoformat()
            }, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        #notify other when leave
        await manager.broadcast({
            "type": "user_left",
            "user_id": user.id,
            "username": user.username,
            "timestamp": datetime.now(timezone.utc).isoformat()
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
    messages = db.query(ChatMessage).filter(
        ChatMessage.room_id == room_id
    ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
    messages.reverse() #chronological order

    return {
        "room_id": room_id,
        "messages": [
            {
                "id": msg.id,
                "user_id": msg.user_id,
                "username": msg.user.username,
                "message": msg.message,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    }

@router.get("/api/chat/rooms")
async def get_available_rooms():
    #real app store in db, now return static list
    rooms = [
        {"id": "math-101", "name": "Math 101 Study Group", "subject": "Mathematics"},
        {"id": "physics-201", "name": "Physics 201", "subject": "Physics"},
        {"id": "cs-fundamentals", "name": "Computer Science Fundamentals", "subject": "CS"},
        {"id": "general", "name": "General Study Hall", "subject": "General"}
    ]
    #add actuve user count
    for room in rooms:
        room["active_users"] = len(manager.get_room_users(room["id"]))
    
    return {"rooms": rooms}
