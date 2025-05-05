from telegram.ext import Application

_application: Application = None

def set_application(app: Application):
    global _application
    _application = app

def get_application() -> Application:
    return _application
