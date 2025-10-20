# --- Imports ---
from sqlalchemy.orm import Session
from . import models as db_models
from ..core import models as pydantic_models

# --- CRUD Functions ---

def save_statement_data(db: Session, data: pydantic_models.StatementData, filename: str) -> db_models.Statement:
    """
    Saves a complete, parsed statement and its transactions to the database.

    Args:
        db (Session): The database session.
        data (pydantic_models.StatementData): The Pydantic model containing the
                                              validated data from the LLM.
        filename (str): The original filename of the uploaded document.

    Returns:
        db_models.Statement: The newly created Statement record from the database.
    """
    print("Saving extracted data to the database...")
    
    # Create the main Statement record, now including the actual filename.
    db_statement = db_models.Statement(
        filename=filename, # <-- THIS IS THE UPDATED LINE
        account_holder=data.account_holder,
        account_number=data.account_number,
        period_start=data.period_start,
        period_end=data.period_end,
        beginning_balance=data.beginning_balance,
        ending_balance=data.ending_balance,
    )
    
    # Create the associated Transaction records.
    for trans in data.transactions:
        db_transaction = db_models.Transaction(
            date=trans.date,
            description=trans.description,
            debit=trans.debit,
            credit=trans.credit,
            balance=trans.balance,
            statement=db_statement # This links the transaction to the statement
        )
        db.add(db_transaction)
        
    # Add the main statement record to the session.
    db.add(db_statement)
    
    # Commit all changes to the database.
    db.commit()
    
    # Refresh the statement object to get its newly assigned ID from the database.
    db.refresh(db_statement)
    
    print(f"Successfully saved Statement ID: {db_statement.id} for file '{filename}' to the database.")
    return db_statement