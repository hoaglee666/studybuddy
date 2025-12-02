from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .config import settings
from .database import engine, Base
from .routers import auth, notes, flashcards, analytics, ai, study_sessions, websocket

#create db table
Base.metadata.create_all(bind=engine)

#create fastapi app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

#cors midd
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#create upload dir if not exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
#mount upload dir for serving
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

#routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(flashcards.router)
app.include_router(ai.router)
app.include_router(websocket.router)
app.include_router(analytics.router_analytics)
app.include_router(study_sessions.router_sessions)

@app.get("/")
async def root():
    return {
        "message": "Welcome to StudyBuddy API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)