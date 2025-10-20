# --- Imports ---
import pandas as pd

# --- Core Function ---
def validate_and_enrich_data(statement_data: dict) -> dict:
    """
    Performs deterministic calculations and enriches the data for the frontend.

    This function takes the clean JSON data from the LLM and performs a final,
    critical validation step: checking if the financial arithmetic is correct.
    It calculates the ending balance based on the transactions and compares it
    to the ending balance extracted by the LLM.

    It also enriches the data with a 'summary' dictionary that the frontend
    can use to display key metrics.

    Args:
        statement_data (dict): The structured data extracted by the LLM.

    Returns:
        dict: The original data, enriched with a 'summary' dictionary containing
              calculated totals and a validation flag.
    """
    print("Performing final validation and data enrichment...")

    # Convert the list of transaction dictionaries into a Pandas DataFrame for easy numerical operations.
    df = pd.DataFrame(statement_data.get('transactions', []))

    # Ensure the debit and credit columns are numeric, coercing errors to NaN and then filling with 0.
    df['credit'] = pd.to_numeric(df['credit'], errors='coerce').fillna(0.0)
    df['debit'] = pd.to_numeric(df['debit'], errors='coerce').fillna(0.0)

    # Calculate the sum of all credits and debits.
    total_credits = df['credit'].sum()
    total_debits = df['debit'].sum()

    # Perform the core financial check.
    calculated_balance = (
        statement_data.get('beginning_balance', 0) + total_credits - total_debits
    )

    # Compare the calculated balance to the statement's ending balance with a small tolerance.
    is_consistent = abs(calculated_balance - statement_data.get('ending_balance', 0)) < 0.01
    
    if is_consistent:
        print("Validation successful: Balances are consistent.")
    else:
        print("Validation FAILED: Calculated balance does not match statement's ending balance.")

    # Add a new 'summary' dictionary to the main data object for the frontend.
    statement_data['summary'] = {
        'total_credits': round(total_credits, 2),
        'total_debits': round(total_debits, 2),
        'calculated_balance': round(calculated_balance, 2),
        'is_consistent': bool(is_consistent)
    }
    
    print("Data enrichment complete.")

    return statement_data