"""WebSocket connection manager for real-time events"""
from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # event_id -> set of websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, event_id: str, websocket: WebSocket):
        await websocket.accept()
        if event_id not in self.active_connections:
            self.active_connections[event_id] = set()
        self.active_connections[event_id].add(websocket)
        logger.info(f"Client connected to event {event_id}")

    def disconnect(self, event_id: str, websocket: WebSocket):
        if event_id in self.active_connections:
            self.active_connections[event_id].discard(websocket)
            if not self.active_connections[event_id]:
                del self.active_connections[event_id]
        logger.info(f"Client disconnected from event {event_id}")

    async def broadcast_event(self, event_id: str, data: dict):
        if event_id in self.active_connections:
            for connection in self.active_connections[event_id]:
                try:
                    await connection.send_json(data)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")

ws_manager = ConnectionManager()

@router.websocket("/ws/events/{event_id}")
async def websocket_endpoint(websocket: WebSocket, event_id: str):
    await ws_manager.connect(event_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or process as needed
    except WebSocketDisconnect:
        ws_manager.disconnect(event_id, websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(event_id, websocket)
