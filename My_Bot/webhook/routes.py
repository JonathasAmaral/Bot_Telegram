from fastapi import APIRouter, Request, Response, HTTPException
from telegram import Update
from telegram.ext import Application
from .app_state import get_application

router = APIRouter()

@router.post("/api/webhook")
async def telegram_webhook(req: Request):
    # Get application instance from state management
    application = get_application()
    if not application:
        raise HTTPException(status_code=503, detail="Bot application not initialized")
    
    # Process Telegram update
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    
    return Response(status_code=200)
