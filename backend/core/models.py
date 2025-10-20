# in backend/core/models.py
from pydantic import BaseModel
from typing import List, Optional

class Transaction(BaseModel):
    date: str
    description: str
    debit: float
    credit: float
    balance: float

class StatementData(BaseModel):
    account_holder: str
    account_number: str
    period_start: str
    period_end: str
    beginning_balance: float
    ending_balance: float
    
    # --- NEW: Add currency symbol field ---
    currency_symbol: Optional[str] = "$" # Default to $ if not found
    
    transactions: List[Transaction]
    warnings: Optional[List[str]] = None