import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.core.logging_config import configure_logging
from backend.api import routes_ocr, routes_health

# Configure logging at startup
configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Document AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan replaces deprecated @app.on_event
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" Application startup: Document AI API is launching")
    yield
    logger.info(" Application shutdown: Document AI API is stopping")

app = FastAPI(title="Document AI API", lifespan=lifespan)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(" Request start: %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info(" Request end: %s %s -> %s", request.method, request.url.path, response.status_code)
        return response
    except Exception as e:
        logger.exception(" Exception during request %s %s: %s", request.method, request.url.path, str(e))
        raise

# Routers
app.include_router(routes_ocr.router, prefix="/api", tags=["OCR"])
app.include_router(routes_health.router, prefix="/api", tags=["Health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
