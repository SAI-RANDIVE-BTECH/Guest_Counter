"""Device management."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.device import Device
from app.config import settings
from app.websocket_manager import ws_manager

router = APIRouter()

class DevicePing(BaseModel):
    event_id: str
    device_id: str
    gate_label: str = "Gate 1"
    direction: str = "idle"

@router.get("/list")
async def list_devices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.is_active == True))
    devices = result.scalars().all()
    return {
        "devices": [
            {
                "id": str(d.id),
                "name": d.name,
                "ip_address": d.ip_address,
                "mode": d.mode,
                "last_seen": d.last_seen.isoformat() if d.last_seen else None,
            }
            for d in devices
        ]
    }

@router.post("/ping")
async def device_ping(
    payload: DevicePing,
    request: Request,
    x_device_secret: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if x_device_secret != settings.DEVICE_SECRET:
        raise HTTPException(status_code=401, detail="Invalid device secret")

    device = await db.scalar(select(Device).where(Device.id == payload.device_id))
    if device:
        device.last_seen = datetime.utcnow()
        device.ip_address = request.client.host if request.client else None
        await db.commit()

    await ws_manager.broadcast_event(payload.event_id, {
        "type": "device_ping",
        "device_id": payload.device_id,
        "gate": payload.gate_label,
        "direction": payload.direction,
        "time": datetime.utcnow().isoformat()
    })

    return {"ok": True, "received": payload.direction}
