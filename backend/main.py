# --- Imports ---
from fastapi import FastAPI
from .api.v1 import endpoints
from .database import database # <-- NEW IMPORT

# --- Create Database Tables ---
# This line tells SQLAlchemy to create all the tables defined in our
# database/models.py file if they don't already exist.
database.Base.metadata.create_all(bind=database.engine)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="IntelliStatement API",
    description="The backend service for the IntelliStatement application, handling PDF/image processing and data extraction.",
    version="1.0.0"
)

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the IntelliStatement Backend API!"}

# --- Include API Routers ---
app.include_router(endpoints.router, prefix="/api/v1", tags=["Processing"])