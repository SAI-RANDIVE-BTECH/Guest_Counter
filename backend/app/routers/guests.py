"""Guest management API"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from datetime import datetime
import uuid, secrets, os, aiofiles
from typing import Optional, List
from PIL import Image
import io
import qrcode

from app.database import get_db
from app.models.guest import Guest, EventGuest, GuestType
from app.ai.face_engine import FaceEngine
from app.utils.jwt import verify_token
from app.config import settings

router = APIRouter()

def generate_guest_code() -> str:
    return f"GV-{secrets.token_hex(3).upper()}"

def get_upload_path(guest_id: str, filename: str) -> str:
    folder = os.path.join(settings.LOCAL_STORAGE_PATH, "guests", str(guest_id))
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)

@router.post("/register")
async def register_guest(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: str = Form(""),
    mobile: str = Form(""),
    email: str = Form(""),
    company: str = Form(""),
    designation: str = Form(""),
    guest_type: str = Form("regular"),
    is_vip: bool = Form(False),
    event_id: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = None
):
    face_engine: FaceEngine = request.app.state.face_engine
    photo_bytes = await photo.read()

    try:
        img = Image.open(io.BytesIO(photo_bytes))
        img.verify()
    except Exception:
        raise HTTPException(400, "Invalid image file")

    embedding, quality = face_engine.extract_embedding(photo_bytes)
    if embedding is None:
        raise HTTPException(422, "No face detected in photo")

    if quality < settings.FACE_QUALITY_MIN:
        raise HTTPException(422, f"Photo quality too low ({quality:.2f})")

    guest_id = uuid.uuid4()
    guest_code = generate_guest_code()
    qr_token = secrets.token_urlsafe(32)

    photo_filename = f"photo_1.jpg"
    photo_path = get_upload_path(str(guest_id), photo_filename)
    async with aiofiles.open(photo_path, 'wb') as f:
        await f.write(photo_bytes)

    qr_data = f"{settings.BACKEND_URL}/api/qr/verify/{qr_token}"
    qr_img = qrcode.make(qr_data, box_size=10, border=4)
    qr_path = get_upload_path(str(guest_id), "qr.png")
    qr_img.save(qr_path)

    guest = Guest(
        id=guest_id,
        guest_code=guest_code,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        mobile=mobile,
        email=email,
        company=company,
        designation=designation,
        guest_type=guest_type,
        is_vip=is_vip,
        photo_paths=[photo_path],
        face_embedding=embedding.tolist(),
        face_embeddings_all=[embedding.tolist()],
        qr_token=qr_token,
        qr_image_path=qr_path,
    )
    db.add(guest)

    if event_id:
        mapping = EventGuest(event_id=uuid.UUID(event_id), guest_id=guest_id)
        db.add(mapping)

    await db.commit()
    await db.refresh(guest)

    return {
        "success": True,
        "guest_id": str(guest.id),
        "guest_code": guest.guest_code,
        "qr_token": qr_token,
        "qr_url": f"/uploads/guests/{guest_id}/qr.png",
        "face_quality": quality,
        "message": f"Guest {first_name} {last_name} registered successfully"
    }

@router.get("/list")
async def list_guests(
    event_id: Optional[str] = None,
    search: Optional[str] = None,
    guest_type: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = None
):
    query = select(Guest).where(Guest.is_deleted == False)

    if search:
        s = f"%{search}%"
        query = query.where(
            Guest.first_name.ilike(s) |
            Guest.last_name.ilike(s) |
            Guest.mobile.ilike(s) |
            Guest.guest_code.ilike(s) |
            Guest.company.ilike(s)
        )

    if guest_type:
        query = query.where(Guest.guest_type == guest_type)

    if event_id:
        query = query.join(EventGuest).where(
            EventGuest.event_id == uuid.UUID(event_id)
        )

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.offset((page-1)*limit).limit(limit))
    guests = result.scalars().all()

    return {
        "guests": [
            {
                "id": str(g.id),
                "guest_code": g.guest_code,
                "name": f"{g.first_name} {g.last_name}",
                "mobile": g.mobile,
                "email": g.email,
                "company": g.company,
                "guest_type": g.guest_type,
                "is_vip": g.is_vip,
                "has_face": g.face_embedding is not None,
                "qr_url": f"/uploads/guests/{g.id}/qr.png" if g.qr_image_path else None,
                "created_at": g.created_at.isoformat()
            }
            for g in guests
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }
