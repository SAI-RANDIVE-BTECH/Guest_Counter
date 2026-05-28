#!/bin/bash
set -e

echo "GuestVision AI Setup"
echo "===================="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Install Docker first."
  exit 1
fi

docker compose version >/dev/null 2>&1 || {
  echo "Docker Compose plugin not found."
  exit 1
}

[ -f backend/.env ] || cp backend/.env.example backend/.env
[ -f frontend/.env ] || cp frontend/.env.example frontend/.env

docker compose up -d --build

echo
echo "Stack started."
echo "Frontend:  http://localhost:5173"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo "Postgres:  localhost:5432"
echo "Redis:     localhost:6379"
echo
echo "Logs: docker compose logs -f"
echo "Stop: docker compose down"
