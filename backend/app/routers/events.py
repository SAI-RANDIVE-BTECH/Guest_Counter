"""Events management"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.database import get_db
from app.models.event import Event

router = APIRouter()

@router.get("/list")
async def list_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.is_active == True))
    events = result.scalars().all()
    return {
        "events": [
            {
                "id": str(e.id),
                "name": e.name,
                "location": e.location,
                "start_date": e.start_date.isoformat() if e.start_date else None,
                "end_date": e.end_date.isoformat() if e.end_date else None,
            }
            for e in events
        ]
    }

@router.get("/{event_id}")
async def get_event(event_id: str, db: AsyncSession = Depends(get_db)):
    event = await db.get(Event, uuid.UUID(event_id))
    if not event:
        raise HTTPException(404, "Event not found")
    return {
        "id": str(event.id),
        "name": event.name,
        "location": event.location,
        "start_date": event.start_date.isoformat() if event.start_date else None,
    }
