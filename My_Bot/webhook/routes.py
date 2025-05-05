from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from telegram import Update
from telegram.ext import Application
from .app_state import get_application
import os
from pathlib import Path

# Import from the new centralized configuration
from config import BOT_TOKEN, WEBHOOK_URL, BASE_DIR, logger

router = APIRouter()

# Health check endpoint para a rota raiz
@router.get("/")
async def root_health_check():
    return JSONResponse({"status": "ok", "message": "Bot is running"})

# Rota para servir arquivos estáticos
@router.get("/api/assets/{folder}/{subfolder}/{filename}")
async def serve_assets(folder: str, subfolder: str, filename: str):
    file_path = BASE_DIR / "api" / "assets" / folder / subfolder / filename
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail=f"Asset not found: {filename}")

@router.post("/api/webhook")
async def telegram_webhook(req: Request):
    # Get the application instance
    application = get_application()
    if not application:
        raise HTTPException(status_code=503, detail="Bot application not initialized")

    # Process Telegram update
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    
    return Response(status_code=200)
