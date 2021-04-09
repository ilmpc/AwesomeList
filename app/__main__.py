import uvicorn
from .config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        debug=settings.debug,
        reload=settings.debug,
        log_level="debug" if settings.debug else "error",
    )
