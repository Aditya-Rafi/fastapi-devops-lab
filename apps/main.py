import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from psycopg2 import connect
from redis import Redis

app = FastAPI()

# Mengambil konfigurasi dari Environment Variables (12-Factor App)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"status": "Senior DevOps App is Running"}

@app.get("/health")
def health_check():
    # 1. Cek Koneksi Redis
    try:
        r = Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=1)
        r.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"

    # 2. Cek Koneksi Postgres
    try:
        conn = connect(DATABASE_URL, connect_timeout=1)
        conn.close()
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    # Jika ada salah satu yang mati, return HTTP 500 (Standard Orchestrator)
    if redis_status == "unhealthy" or db_status == "unhealthy":
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "redis": redis_status, "database": db_status},
        )

    return {"status": "healthy", "redis": redis_status, "database": db_status}
