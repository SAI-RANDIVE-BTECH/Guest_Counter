"""QR code generation and verification"""
from fastapi import APIRouter, Depends, HTTPException, Form, Header
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
import uuid, os

from app.database import get_db
from app.models.guest import Guest, AttendanceLog, EventGuest
from app.websocket_manager import ws_manager
from app.config import settings

router = APIRouter()

@router.get("/download/{guest_id}")
async def download_qr(guest_id: str, db: AsyncSession = Depends(get_db)):
    """Download QR code for guest"""
    guest = await db.get(Guest, uuid.UUID(guest_id))
    if not guest:
        raise HTTPException(404, "Guest not found")
    if not guest.qr_image_path or not os.path.exists(guest.qr_image_path):
        raise HTTPException(404, "QR not generated")
    return FileResponse(guest.qr_image_path, media_type="image/png")

@router.post("/scan")
async def scan_qr(
    event_id: str = Form(...),
    device_id: str = Form(...),
    gate_label: str = Form("Gate 1"),
    qr_payload: str = Form(...),
    x_device_secret: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if x_device_secret != settings.DEVICE_SECRET:
        raise HTTPException(401)

    token = qr_payload.split("/")[-1]
    guest = await db.scalar(select(Guest).where(Guest.qr_token == token))
    if not guest:
        return {"result": "invalid_qr"}

    mapping = await db.scalar(
        select(EventGuest).where(
            and_(
                EventGuest.event_id == uuid.UUID(event_id),
                EventGuest.guest_id == guest.id
            )
        )
    )
    if not mapping:
        return {"result": "not_invited", "guest": guest.first_name}

    cutoff = datetime.utcnow() - timedelta(minutes=10)
    recent = await db.scalar(
        select(AttendanceLog).where(
            and_(
                AttendanceLog.guest_id == guest.id,
                AttendanceLog.event_id == uuid.UUID(event_id),
                AttendanceLog.entry_time >= cutoff,
                AttendanceLog.is_duplicate == False
            )
        )
    )
    is_dup = recent is not None

    log = AttendanceLog(
        event_id=uuid.UUID(event_id),
        guest_id=guest.id,
        device_id=uuid.UUID(device_id),
        verify_mode="qr",
        confidence=1.0,
        is_duplicate=is_dup,
        gate_label=gate_label
    )
    db.add(log)
    await db.commit()

    await ws_manager.broadcast_event(event_id, {
        "type": "guest_arrived" if not is_dup else "duplicate",
        "guest_name": f"{guest.first_name} {guest.last_name}",
        "verify_mode": "qr",
        "gate": gate_label
    })

    return {
        "result": "duplicate" if is_dup else "match",
        "guest_name": f"{guest.first_name} {guest.last_name}",
        "guest_code": guest.guest_code,
        "is_vip": guest.is_vip
    }
