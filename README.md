"# GuestVision AI - Smart Event Guest Management System

> **AI-Powered, Real-Time Guest Recognition & Attendance Tracking**

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker Ready](https://img.shields.io/badge/docker-ready-brightgreen.svg)](docker-compose.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)

## 🎯 Overview

**GuestVision AI** is a comprehensive, production-ready event management platform that combines:

- **🤖 AI Face Recognition** - Real-time guest identification using InsightFace with 512D embeddings
- **📱 Mobile-First Frontend** - Next.js dashboard with live counters and real-time WebSocket updates
- **⚡ FastAPI Backend** - High-performance async Python API with PostgreSQL + Redis
- **🔌 IoT Integration** - PlatformIO firmware for AMB82 Mini microcontroller with WiFi provisioning
- **🐳 Docker Orchestration** - Complete containerized stack (PostgreSQL, Redis, Backend, Frontend)
- **📊 Real-Time Analytics** - Live dashboard showing arrival stats, duplicates, unknown faces

Perfect for:
- ✨ Corporate events & conferences
- 🎉 Weddings & social gatherings
- 🏢 Venue access control
- 🎪 Festival/festival crowd management

---

## ⚡ Quick Start (Docker)

### Prerequisites
- **Docker** & **Docker Compose** ([Install](https://docs.docker.com/get-docker/))
- **Git** ([Install](https://git-scm.com/))

### Setup & Run (5 minutes)

```bash
# Clone repository
git clone https://github.com/SAI-RANDIVE-BTECH/Guest_Counter.git
cd Guest_Counter

# Create environment file
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Update backend/.env with required values:
# DATABASE_URL=postgresql://postgres:postgres@postgres:5432/guestvision
# REDIS_URL=redis://redis:6379
# SECRET_KEY=your-secret-key-here
# INSIGHTFACE_MODEL=buffalo_l

# Start services
docker-compose up -d

# Wait for services to initialize (30 seconds)
sleep 30

# Access applications
```

### 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:3000 | See below |
| **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |
| **API ReDoc** | http://localhost:8000/redoc | Detailed API reference |
| **PostgreSQL** | localhost:5432 | User: postgres / Password: postgres |
| **Redis** | localhost:6379 | No auth (dev only) |

### 📝 First Login

1. Navigate to http://localhost:3000
2. Create admin account (first-time setup)
3. Create event in dashboard
4. Register guests with camera capture
5. View real-time arrival dashboard

---

## 🏗️ Project Structure

```
Guest_Counter/
├── backend/                    # FastAPI Python backend
│   ├── main.py                # Application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container build config
│   ├── app/
│   │   ├── config.py          # Configuration & environment variables
│   │   ├── database.py        # SQLAlchemy async engine & session
│   │   ├── models/            # SQLAlchemy ORM models
│   │   │   ├── guest.py       # Guest table & EventGuest join
│   │   │   ├── event.py       # Event table
│   │   │   ├── user.py        # User table
│   │   │   ├── device.py      # Device table (AMB82 mini)
│   │   │   └── unknown_face.py # Unknown faces captured
│   │   ├── routers/           # API route handlers
│   │   │   ├── guests.py      # Guest CRUD & enrollment
│   │   │   ├── recognition.py # Face recognition endpoint
│   │   │   ├── qr.py          # QR code generation/scanning
│   │   │   ├── events.py      # Event management
│   │   │   ├── dashboard.py   # Statistics & counters
│   │   │   └── auth.py        # Authentication & login
│   │   ├── ai/
│   │   │   └── face_engine.py # InsightFace wrapper & embeddings
│   │   ├── utils/
│   │   │   ├── jwt.py         # JWT token & password hashing
│   │   │   └── validators.py  # Input validation
│   │   └── websocket_manager.py # Real-time event broadcasting
│   └── db/
│       ├── schema.sql         # Database schema
│       └── migration.sql      # Migration scripts
│
├── frontend/                   # Next.js React frontend
│   ├── package.json           # NPM dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── vite.config.ts         # Build configuration
│   ├── Dockerfile             # Container build config
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout wrapper
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx           # Live counter dashboard
│   │   │   │   └── guests/
│   │   │   │       └── new/page.tsx   # Guest registration form
│   │   │   └── page.tsx       # Home page
│   │   ├── components/
│   │   │   └── CameraCapture.tsx # Mobile camera component
│   │   ├── lib/
│   │   │   ├── api.ts         # API client utilities
│   │   │   └── socket.ts      # Socket.IO client
│   │   └── styles/            # CSS modules
│   └── .env.local.example     # Environment template
│
├── firmware/                   # PlatformIO AMB82 Mini firmware
│   ├── platformio.ini         # Build configuration
│   ├── src/
│   │   └── main.cpp           # Arduino C++ firmware
│   └── lib/
│       └── README             # Library documentation
│
├── docker-compose.yml          # Multi-container orchestration
├── .gitignore                 # Git exclusions (secrets, deps)
└── README.md                  # This file
```

---

## 🚀 Core Features

### 👥 Guest Management
- **Enrollment**: Register guests with photo capture & face embedding extraction
- **QR Generation**: Unique QR code per guest (downloadable PNG)
- **Search**: Filter guests by event, name, VIP status
- **Deduplication**: Automatic duplicate detection (configurable cooldown)

### 🤖 AI Face Recognition
- **Real-Time Detection**: Process JPEG frames from IoT device
- **Embedding Extraction**: 512-dimensional L2-normalized vectors via InsightFace
- **Similarity Matching**: Cosine similarity search with configurable threshold (default 0.45)
- **Quality Scoring**: 0-1 score based on:
  - Face detection confidence
  - Face size in frame
  - Head pose angle
  - Face centrality
- **Unknown Face Capture**: Snapshot storage for unrecognized guests

### 📊 Live Dashboard
- **Real-Time Counters**: 
  - Total arrived / Total invited
  - Remaining guests
  - Duplicate attempts
  - Unknown faces detected
  - VIP arrivals
  - Face vs QR entries
- **Activity Log**: Last 50 arrival events with timestamps
- **Event Selector**: Switch between multiple simultaneous events
- **Connection Status**: WebSocket indicator for live updates

### 🔌 IoT Integration
- **WiFi Provisioning**: Soft AP on first boot (SSID: GuestVision-Setup)
- **Configuration Portal**: Web UI for WiFi & server settings
- **Frame Capture**: Regular JPEG snapshots to backend
- **LED Feedback**: Status indicators (red/green GPIO pins)
- **Persistent Storage**: NVS (Preferences library) for credentials

### 🔐 Security
- **JWT Authentication**: Signed tokens with configurable expiry
- **Password Hashing**: bcrypt with salt
- **CORS Protection**: Configurable allowed origins
- **Rate Limiting**: Per-endpoint request throttling (implementable)
- **Environment Secrets**: .env files excluded from git

---

## 🛠️ API Endpoints

### Authentication
```
POST   /api/auth/login              # Login with credentials
GET    /api/auth/me                 # Get current user info
POST   /api/auth/refresh            # Refresh JWT token
```

### Guest Management
```
POST   /api/guests/register         # Register new guest (multipart form)
GET    /api/guests/list             # List guests (with search & pagination)
GET    /api/guests/{guest_id}       # Get guest details
PUT    /api/guests/{guest_id}       # Update guest info
DELETE /api/guests/{guest_id}       # Remove guest
```

### Face Recognition
```
POST   /api/recognize/face          # Main recognition endpoint (from device)
                                    # Input: JPEG frame, device_id, event_id, gate_label
                                    # Output: {status, guest_id, confidence, is_duplicate}
```

### QR Code
```
GET    /api/qr/download/{guest_id}  # Download QR code PNG
POST   /api/qr/scan                 # Verify scanned QR token
```

### Events
```
GET    /api/events/list             # List all events
GET    /api/events/{event_id}       # Get event details
POST   /api/events                  # Create event
PUT    /api/events/{event_id}       # Update event
```

### Dashboard
```
GET    /api/dashboard/counters/{event_id}  # Get live statistics
```

### WebSocket (Real-Time)
```
WS     /ws/events/{event_id}        # Subscribe to event updates
       Events: guest_arrived, duplicate, unknown_face
```

---

## 🗄️ Database Schema

### Core Tables

**guests**
- `id` (UUID, PK)
- `guest_code` (String, unique) - Human-readable ID
- `first_name`, `last_name`
- `mobile` (Phone)
- `face_embedding` (JSON) - 512D vector
- `photo_paths` (JSON) - Array of uploaded photo URLs
- `is_vip` (Boolean)
- `created_at`, `updated_at` (Timestamp)

**events**
- `id` (UUID, PK)
- `name`, `description`
- `date_start`, `date_end` (Datetime)
- `face_threshold` (Float) - Confidence threshold for this event
- `duplicate_cooldown_mins` (Integer)
- `is_active` (Boolean)
- `created_at`, `updated_at`

**event_guests** (Join table)
- `event_id` (UUID, FK → events)
- `guest_id` (UUID, FK → guests)
- `is_invited` (Boolean)
- `invited_date` (Timestamp)

**attendance_logs**
- `id` (UUID, PK)
- `event_id`, `guest_id` (FKs)
- `verify_mode` (Enum: 'face' | 'qr')
- `confidence` (Float) - For face matches
- `is_duplicate` (Boolean)
- `gate_label` (String) - Gate/location identifier
- `timestamp` (Datetime)

**users**
- `id` (UUID, PK)
- `username`, `email` (Unique)
- `hashed_password`
- `is_admin` (Boolean)
- `created_at`

**devices** (IoT devices)
- `id` (UUID, PK)
- `device_token` (String, unique)
- `ip_address`
- `mode` (String) - Device mode
- `last_seen` (Datetime)

**unknown_faces**
- `id` (UUID, PK)
- `event_id` (UUID, FK)
- `photo_url` (String)
- `confidence` (Float)
- `timestamp` (Datetime)

---

## 🤖 AI Model Specifications

### InsightFace Configuration
- **Model**: buffalo_l (ArcFace R100)
- **Embedding Dimension**: 512
- **Normalization**: L2 (unit vectors)
- **Similarity Metric**: Cosine distance
- **Detection Backend**: RetinaFace

### Face Quality Scoring
```
quality = (
  0.40 * detection_confidence +
  0.25 * face_size_ratio +
  0.20 * pose_quality +
  0.15 * face_centrality
)
```
- **Minimum Quality Threshold**: 0.5 (0-1 scale)
- **Default Match Threshold**: 0.45 cosine similarity
- **Tunable Per Event**: Via `event.face_threshold`

### Performance Characteristics
- **Inference Time**: ~100ms per frame (GPU) / ~500ms (CPU)
- **Model Size**: ~130MB (buffalo_l)
- **Memory Footprint**: ~400MB loaded
- **Concurrent Requests**: 10+ via async workers

---

## 📚 Local Development

### Prerequisites
- **Python 3.11+** ([Download](https://www.python.org/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **PostgreSQL 15** ([Download](https://www.postgresql.org/))
- **Redis 7** ([Download](https://redis.io/))
- **PlatformIO CLI** (for firmware)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python -c "from app.database import init_db; init_db()"

# Download InsightFace model
python -c "from app.ai.face_engine import load_model; load_model()"

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# API docs available at http://localhost:8000/docs
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Update NEXT_PUBLIC_API_URL to your backend URL

# Start development server
npm run dev

# Open http://localhost:3000
```

### Firmware Setup

```bash
cd firmware

# Install PlatformIO CLI
pip install platformio

# Configure board settings in platformio.ini
# Build firmware
pio run

# Upload to device
pio run --target upload

# Monitor serial output
pio device monitor
```

---

## 🐳 Docker Deployment

### Production Deployment

```bash
# Build images
docker-compose build

# Start services with health checks
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Environment Configuration

Create `.env` file in project root:
```bash
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=guestvision

# Backend
DATABASE_URL=postgresql://postgres:secure_password_here@postgres:5432/guestvision
REDIS_URL=redis://redis:6379
SECRET_KEY=your-super-secret-key-generate-with-openssl
INSIGHTFACE_MODEL=buffalo_l
FACE_THRESHOLD=0.45
LOCAL_STORAGE_PATH=/opt/guestvision/uploads

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Health Checks
All services include health checks:
```bash
# Check if all services are healthy
docker-compose ps

# Check specific service logs
docker-compose logs postgres  # Verify DB connection
docker-compose logs backend   # Check startup errors
```

---

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `REDIS_URL` | Required | Redis connection string |
| `SECRET_KEY` | Required | JWT signing secret (min 32 chars) |
| `INSIGHTFACE_MODEL` | buffalo_l | AI model type |
| `FACE_THRESHOLD` | 0.45 | Default face match confidence |
| `DUPLICATE_COOLDOWN` | 10 | Minutes before same guest can re-enter |
| `LOCAL_STORAGE_PATH` | /opt/uploads | Photo storage directory |
| `BACKEND_URL` | http://localhost:8000 | Public backend URL |
| `DEVICE_SECRET` | random | Device authentication token |

### Frontend Configuration (`frontend/.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | http://localhost:8000 | Backend API base URL |
| `NEXT_PUBLIC_WS_URL` | ws://localhost:8000 | WebSocket URL |

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Database Connection Error**
```
error: could not connect to server: Connection refused
```
**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Verify DATABASE_URL in backend/.env
```

#### 2. **Face Recognition Not Working**
```
error: InsightFace model not found
```
**Solution:**
```bash
# Manually download model
python -c "from insightface.app import FaceAnalysis; fa = FaceAnalysis(name='buffalo_l'); fa.prepare(ctx_id=0, det_model='retinaface')"

# Verify model directory
ls ~/.insightface/models/
```

#### 3. **WebSocket Connection Timeout**
```
Failed to connect to WebSocket
```
**Solution:**
```bash
# Check CORS settings in backend
# Verify frontend NEXT_PUBLIC_WS_URL matches backend host

# Check firewall allows WebSocket on port 8000
netstat -an | grep 8000
```

#### 4. **Camera Not Working on Mobile**
```
getUserMedia not supported / Permission denied
```
**Solution:**
- Ensure site is served over HTTPS (or localhost)
- Grant camera permission in browser settings
- Test on Android Chrome or iOS Safari (latest versions)

#### 5. **PlatformIO Build Fails**
```
error: unable to write file - No space left on device
```
**Solution:**
```bash
# Clear PlatformIO cache
platformio cache clean

# Move cache to external drive (if low on C:)
setx PLATFORMIO_HOME E:\.platformio

# Or use Docker-based build
docker-compose up backend frontend  # Skip firmware
```

---

## 📈 Performance Tips

### Backend Optimization
- **Connection Pooling**: Tune `pool_size` in `config.py` (default: 20)
- **Caching**: Redis caching for guest embeddings
- **Async Processing**: All I/O operations are async
- **Model Optimization**: Use GPU (CUDA) for faster inference

### Frontend Optimization
- **Image Optimization**: Next.js Image component for photos
- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Components load on-demand
- **WebSocket Batching**: Combine multiple events

### Database Optimization
- **Indexes**: Already created on `guest_code`, `email`, `event_id`
- **Query Optimization**: Use pagination for large result sets
- **Connection Pooling**: Configured with async_mode

---

## 🔐 Security Checklist

- [ ] Change default PostgreSQL password in `.env`
- [ ] Generate strong `SECRET_KEY` (use `openssl rand -base64 32`)
- [ ] Enable HTTPS in production
- [ ] Use environment variables for all secrets
- [ ] Implement rate limiting on API endpoints
- [ ] Set up database backups
- [ ] Enable CORS only for trusted origins
- [ ] Implement request logging & monitoring
- [ ] Regular security updates for dependencies

---

## 📞 Support & Contribution

### Getting Help
- Check [Troubleshooting](#-troubleshooting) section
- Review API documentation at `/docs` endpoint
- Check Docker logs: `docker-compose logs -f`
- Review GitHub Issues for known problems

### Contributing
```bash
# Fork repository
git clone https://github.com/YOUR_USERNAME/Guest_Counter.git

# Create feature branch
git checkout -b feature/your-feature

# Make changes, commit, push
git push origin feature/your-feature

# Create Pull Request on GitHub
```

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced analytics & reporting
- [ ] SMS/Email notifications
- [ ] Multi-location events
- [ ] Custom facial recognition models
- [ ] Integration with event ticketing systems
- [ ] WhatsApp verification
- [ ] Machine learning-based duplicate detection

---

## 👨‍💻 Author

**SAI RANDIVE** - [GitHub](https://github.com/SAI-RANDIVE-BTECH)

---

## 🙏 Acknowledgments

- **InsightFace** - Face recognition models
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework for production
- **PostgreSQL** - Reliable database
- **Docker** - Containerization platform

---

## 📞 Contact

For inquiries, features, or support:
- 📧 Email: your-email@example.com
- 🐙 GitHub Issues: [Report Bug](https://github.com/SAI-RANDIVE-BTECH/Guest_Counter/issues)
- 💬 Discussions: [Join Community](https://github.com/SAI-RANDIVE-BTECH/Guest_Counter/discussions)

---

**Built with ❤️ for event management enthusiasts**" 
