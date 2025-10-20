# --- Imports ---
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Database Configuration ---
# Define the connection URL for our SQLite database.
# 'sqlite:///./intellistatement.db' means the database will be a single file
# named 'intellistatement.db' in the root directory of the project.
DATABASE_URL = "sqlite:///./intellistatement.db"

# Create the SQLAlchemy engine. The engine is the entry point to the database.
# The 'connect_args' are needed only for SQLite to allow multithreaded access.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of this class will be a new
# database session. This is how we'll interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class. Our database model classes will inherit from this class.
Base = declarative_base()

# --- Dependency for FastAPI ---
def get_db():
    """
    A dependency function to get a database session for each API request.
    It ensures that the database connection is always closed after the request
    is finished, even if there was an error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  