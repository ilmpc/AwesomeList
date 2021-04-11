import uvicorn
from .config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.PORT,
        debug=settings.DEBUG,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "error",
    )
