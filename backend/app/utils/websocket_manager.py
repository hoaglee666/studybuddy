from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        #room_id -> list of websoc connects
        self.active_connections: Dict[str, List[WebSocket]] = {}
        #websoc -> user_id mapp
        self.user_connections: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: int):
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        
        self.active_connections[room_id].append(websocket)
        self.user_connections[websocket] = user_id
    
    def disconnect(self, websocket: WebSocket, room_id: str,):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
            #remove empty room
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        if websocket in self.user_connections:
            del self.user_connections[websocket]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict, room_id: str):
        if room_id in self.active_connections:
            message_str = json.dumps(message)
            for connection in self.active_connections[room_id]:
                await connection.send_text(message_str)

    def get_room_users(self, room_id: str) -> List[int]:
        if room_id not in self.active_connections:
            return []

        user_ids = []
        for ws in self.active_connections[room_id]:
            if ws in self.user_connections:
                user_ids.append(self.user_connections[ws])
        return user_ids
    
manager = ConnectionManager()