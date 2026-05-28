# GuestVision AI Upload and Run Guide

## 1. Fill Environment Values

Backend:

```powershell
cd E:\Guest_Counter\backend
notepad .env
```

Set real values for:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEVICE_SECRET`
- `BACKEND_URL`
- `FRONTEND_URL`

Frontend:

```powershell
cd E:\Guest_Counter\frontend
notepad .env
```

Set:

- `VITE_API_URL=http://YOUR_BACKEND_IP:8000`
- `VITE_WS_URL=ws://YOUR_BACKEND_IP:8000/ws/events`

Firmware:

```powershell
notepad E:\Guest_Counter\firmware\platformio.ini
```

Replace:

- `GV_WIFI_SSID`
- `GV_WIFI_PASS`
- `GV_SERVER_HOST`
- `GV_DEVICE_SECRET`
- `GV_DEVICE_ID`
- `GV_EVENT_ID`
- `GV_GATE_LABEL`

`GV_DEVICE_SECRET` must match backend `.env`.

## 2. Start Local Backend

```powershell
cd E:\Guest_Counter\backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

For production face recognition on Python 3.11:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-ai.txt
```

Keep `LOAD_FACE_ENGINE_ON_STARTUP=true` after AI packages are installed.

## 3. Start Frontend

```powershell
cd E:\Guest_Counter\frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## 4. Upload Firmware to AMB82 Mini

Install VS Code PlatformIO first, then:

```powershell
cd E:\Guest_Counter\firmware
pio run -t upload
pio device monitor -b 115200
```

Or in VS Code:

1. Open `E:\Guest_Counter\firmware`
2. Open `platformio.ini`
3. Confirm the environment is `amb82-mini`
4. Click PlatformIO Upload
5. Open Serial Monitor at `115200`

Expected boot output:

```text
GuestVision AI AMB82 Mini firmware
[WiFi] Connected: 192.168.x.x
```

If WiFi values are blank or wrong, the device starts AP mode:

```text
SSID: GuestVision-Setup
Password: setup1234
URL: http://192.168.1.1
```

The AP page shows the values that must be compiled into `platformio.ini`.

## 5. Docker Run

```powershell
cd E:\Guest_Counter
docker compose up --build
```

Services:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## 6. Hardware Pins

| Component | AMB82 Pin |
|---|---|
| Display CS | PA_12 |
| Display CLK | PA_13 |
| Display MOSI | PA_14 |
| Display MISO | PA_15 |
| Display DC | PA_25 |
| Display RST | PA_26 |
| Touch CS | PA_22 |
| Touch IRQ | PA_23 |
| Ultrasonic 1 TRIG | PB_18 |
| Ultrasonic 1 ECHO | PB_19 through divider |
| Ultrasonic 2 TRIG | PB_20 |
| Ultrasonic 2 ECHO | PB_21 through divider |
| Green LED | PB_22 |
| Yellow LED | PB_23 |
| Red LED | PB_24 |
| Blue LED | PB_25 |

## 7. Final Production Checklist

- Use Python 3.11 for the AI backend host.
- Install `requirements.txt` and `requirements-ai.txt`.
- Use PostgreSQL and Redis from Docker or managed cloud services.
- Replace all placeholder UUIDs with database-created event/device IDs.
- Keep AMB82, backend, and operator device on the same trusted network unless you deploy HTTPS and proper device auth.
- Do not expose the AMB82 directly to the public internet.
