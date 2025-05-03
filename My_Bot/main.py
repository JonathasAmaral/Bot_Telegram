import os
import logging
import asyncio
import sys

from fastapi import FastAPI
from telegram.ext import Application

from api.bot import create_bot
from webhook.routes import router
from webhook.token import WEBHOOK_URL
from webhook.app_state import set_application

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger("telegram-bot")

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    application = await create_bot()
    await application.bot.set_webhook(WEBHOOK_URL)
    set_application(application)
    logger.info("🤖 Bot iniciado com sucesso.")

@app.on_event("shutdown")
async def on_shutdown():
    from webhook.app_state import get_application
    application = get_application()
    if application:
        await application.shutdown()
        logger.info("🤖 Bot desligado com sucesso.")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
