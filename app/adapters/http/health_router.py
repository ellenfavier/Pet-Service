from fastapi import APIRouter
from pymongo import MongoClient
from app.settings import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """Simple liveness check."""
    return {"status": "ok"}

@router.get("/health/db")
def health_check_db():
    """
    Database connectivity check (Required by assignment).
    """
    try:
        # Create a temporary client with a short timeout
        client = MongoClient(
            settings.MONGO_URI, 
            serverSelectionTimeoutMS=5000
        )
        # Check connection using 'ping'
        client.admin.command('ping')
        return {"status": "ok", "db_connection": "successful"}
    except Exception as e:
        return {"status": "error", "db_connection": "failed", "detail": str(e)}