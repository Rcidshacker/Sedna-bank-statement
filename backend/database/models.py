# --- Imports ---
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# --- SQLAlchemy Table Models ---

class Statement(Base):
    """Defines the 'statements' table in the database."""
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    account_holder = Column(String)
    account_number = Column(String)
    period_start = Column(String)
    period_end = Column(String)
    beginning_balance = Column(Float)
    ending_balance = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # This creates the one-to-many relationship.
    # A single Statement can have multiple Transaction records.
    transactions = relationship("Transaction", back_populates="statement")

class Transaction(Base):
    """Defines the 'transactions' table in the database."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    description = Column(String)
    debit = Column(Float)
    credit = Column(Float)
    balance = Column(Float)
    
    # This is the foreign key that links a transaction back to a statement.
    statement_id = Column(Integer, ForeignKey("statements.id"))
    
    # This defines the many-to-one relationship back to the Statement.
    statement = relationship("Statement", back_populates="transactions")