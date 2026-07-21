"""VoiceSync AI - Main FastAPI Application"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes import auth, dubbing, jobs, voices, health
from app.utils.logging_config import setup_logging
from app.utils.database import init_db

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    logger.info("🚀 VoiceSync AI Backend Starting...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
    
    yield
    
    logger.info("⏹️  VoiceSync AI Backend Shutting Down...")


app = FastAPI(
    title="VoiceSync AI API",
    description="AI-powered video dubbing and lip-sync platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status": "error"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status": "error"},
    )


app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(dubbing.router, prefix="/api/v1/dubbing", tags=["Dubbing"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(voices.router, prefix="/api/v1/voices", tags=["Voices"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to VoiceSync AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "services": {
            "authentication": "✅ Active",
            "dubbing": "✅ Active",
            "transcription": "🔄 Ready",
            "translation": "🔄 Ready",
            "voice_synthesis": "🔄 Ready",
            "lip_sync": "🔄 Ready"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
