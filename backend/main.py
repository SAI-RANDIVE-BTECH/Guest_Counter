from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.database import init_db
from app.ai.face_engine import FaceEngine
from app.routers import auth, events, guests, recognition, qr, devices, dashboard
from app.websocket_manager import router as ws_router
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

face_engine: FaceEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global face_engine
    logger.info("🚀 Starting GuestVision AI...")
    if settings.INIT_DB_ON_STARTUP:
        await init_db()
    face_engine = FaceEngine()
    if settings.LOAD_FACE_ENGINE_ON_STARTUP:
        try:
            face_engine.load_model()
            logger.info("✅ Face engine loaded")
        except Exception:
            logger.exception("Face engine failed to load")
            if settings.STRICT_AI_STARTUP:
                raise
    app.state.face_engine = face_engine
    yield
    logger.info("🛑 Shutting down...")

app = FastAPI(
    title="GuestVision AI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.LOCAL_STORAGE_PATH), name="uploads")

# Register routers
app.include_router(events.router,      prefix="/api/events",      tags=["events"])
app.include_router(auth.router,        prefix="/api/auth",        tags=["auth"])
app.include_router(guests.router,      prefix="/api/guests",      tags=["guests"])
app.include_router(recognition.router, prefix="/api/recognize",   tags=["recognition"])
app.include_router(qr.router,          prefix="/api/qr",           tags=["qr"])
app.include_router(devices.router,     prefix="/api/devices",      tags=["devices"])
app.include_router(dashboard.router,   prefix="/api/dashboard",    tags=["dashboard"])
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"service": "GuestVision AI", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
