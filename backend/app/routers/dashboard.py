"""Dashboard counters and stats"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid

from app.database import get_db
from app.models.guest import AttendanceLog
from app.models.event import Event

router = APIRouter()

@router.get("/counters/{event_id}")
async def get_counters(event_id: str, db: AsyncSession = Depends(get_db)):
    event_uuid = uuid.UUID(event_id)
    
    # Count invited guests
    result = await db.execute(
        select(func.count(AttendanceLog.id)).where(
            AttendanceLog.event_id == event_uuid
        )
    )
    total_arrived = result.scalar() or 0
    
    # Count duplicate attempts
    result = await db.execute(
        select(func.count(AttendanceLog.id)).where(
            and_(
                AttendanceLog.event_id == event_uuid,
                AttendanceLog.is_duplicate == True
            )
        )
    )
    duplicates = result.scalar() or 0

    return {
        "total_invited": 100,  # placeholder
        "total_arrived": total_arrived,
        "remaining": 100 - total_arrived,
        "duplicate_attempts": duplicates,
        "unknown_faces": 0,
        "vip_arrivals": 0,
        "face_entries": total_arrived,
        "qr_entries": 0
    }
