"""Recognition endpoint for AMB82 device"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
import numpy as np
import uuid, aiofiles, os, secrets

from app.database import get_db
from app.models.guest import Guest, EventGuest, AttendanceLog
from app.models.event import Event
from app.models.unknown_face import UnknownFace
from app.ai.face_engine import FaceEngine
from app.websocket_manager import ws_manager
from app.config import settings

router = APIRouter()

@router.post("/face")
async def recognize_face(
    request: Request,
    event_id: str = Form(...),
    device_id: str = Form(...),
    gate_label: str = Form("Gate 1"),
    frame: UploadFile = File(...),
    x_device_secret: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if x_device_secret != settings.DEVICE_SECRET:
        raise HTTPException(401, "Invalid device secret")

    face_engine: FaceEngine = request.app.state.face_engine
    frame_bytes = await frame.read()

    event = await db.scalar(select(Event).where(Event.id == uuid.UUID(event_id)))
    if not event:
        return {"result": "error", "message": "Event not found"}

    threshold = event.face_threshold or 0.45

    embedding, quality = face_engine.extract_embedding(frame_bytes)
    if embedding is None:
        return {"result": "no_face", "message": "No face in frame"}

    result = await db.execute(
        select(Guest).join(EventGuest).where(
            and_(
                EventGuest.event_id == uuid.UUID(event_id),
                Guest.face_embedding != None,
                Guest.is_deleted == False
            )
        )
    )
    guests = result.scalars().all()

    if not guests:
        return {"result": "no_guests", "message": "No guests with face data"}

    guest_ids = [g.id for g in guests]
    embeddings_matrix = np.array([g.face_embedding for g in guests])

    query_norm = embedding / (np.linalg.norm(embedding) + 1e-8)
    db_norms = embeddings_matrix / (np.linalg.norm(embeddings_matrix, axis=1, keepdims=True) + 1e-8)
    similarities = db_norms @ query_norm
    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])

    if best_score < threshold:
        snap_path = f"{settings.LOCAL_STORAGE_PATH}/unknown/{secrets.token_hex(8)}.jpg"
        os.makedirs(os.path.dirname(snap_path), exist_ok=True)
        async with aiofiles.open(snap_path, 'wb') as f:
            await f.write(frame_bytes)
        unknown = UnknownFace(
            event_id=uuid.UUID(event_id),
            device_id=uuid.UUID(device_id),
            snapshot_path=snap_path,
            confidence=best_score
        )
        db.add(unknown)
        await db.commit()
        await ws_manager.broadcast_event(event_id, {
            "type": "unknown_face",
            "score": best_score,
            "gate": gate_label
        })
        return {"result": "unknown", "confidence": best_score}

    matched_guest = guests[best_idx]

    cooldown_mins = event.duplicate_cooldown_mins or 10
    cutoff = datetime.utcnow() - timedelta(minutes=cooldown_mins)
    recent = await db.scalar(
        select(AttendanceLog).where(
            and_(
                AttendanceLog.guest_id == matched_guest.id,
                AttendanceLog.event_id == uuid.UUID(event_id),
                AttendanceLog.entry_time >= cutoff,
                AttendanceLog.is_duplicate == False
            )
        )
    )

    is_dup = recent is not None

    log = AttendanceLog(
        event_id=uuid.UUID(event_id),
        guest_id=matched_guest.id,
        device_id=uuid.UUID(device_id),
        verify_mode="face",
        confidence=best_score,
        is_duplicate=is_dup,
        gate_label=gate_label,
    )
    db.add(log)
    await db.commit()

    await ws_manager.broadcast_event(event_id, {
        "type": "guest_arrived" if not is_dup else "duplicate",
        "guest_name": f"{matched_guest.first_name} {matched_guest.last_name}",
        "guest_code": matched_guest.guest_code,
        "is_vip": matched_guest.is_vip,
        "confidence": best_score,
        "gate": gate_label,
        "time": datetime.utcnow().isoformat()
    })

    return {
        "result": "duplicate" if is_dup else "match",
        "guest_name": f"{matched_guest.first_name} {matched_guest.last_name}",
        "guest_code": matched_guest.guest_code,
        "is_vip": matched_guest.is_vip,
        "confidence": round(best_score, 4),
        "is_duplicate": is_dup
    }
