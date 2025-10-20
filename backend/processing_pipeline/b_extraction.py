# --- Imports ---
import openai
from ..core.models import StatementData
from ..core.config import settings
from typing import List, Dict

# --- LLM Client Initialization ---
# Configure the client once to be reused for all API calls.
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY,
)

# --- Core Orchestration Function ---

def extract_data_with_llm(page_data: List[Dict]) -> dict:
    """
    Processes a list of page data dictionaries by combining them into a single context
    and then using a comprehensive, single-shot LLM prompt for extraction.
    """
    print("Initializing single-prompt LLM extraction...")
    
    if not page_data:
        raise ValueError("Cannot process an empty document.")

    # --- Step 1: Aggregate Page Texts ---
    # Combine the 'text' from each page dictionary into a single string, clearly
    # marking the page breaks. This gives the LLM full context of the entire document.
    print(f"Aggregating {len(page_data)} pages into a single context for the LLM.")
    full_document_text = "\n\n--- Page Break ---\n\n".join([page['text'] for page in page_data])

    # --- Step 2: Use Your Powerful, All-in-One Prompt ---
    # This prompt is used exactly as you designed it, now with the complete
    # document text passed into it.
    prompt = f"""
You are an expert financial analyst AI specialized in parsing diverse financial statements, including traditional bank statements (e.g., checking/savings accounts with balances), digital payment apps (e.g., Google Pay UPI transactions without running balances), credit card summaries, and hybrid formats from PDFs. These may be scanned, tabular, narrative, list-based, or semi-structured, with variations in layouts, currencies (₹, $, £, etc.), date formats (e.g., "01 Sep, 2025", "mm/dd/yyyy", "DD Month YYYY"), abbreviations (UPI, BACS, DD), and noise (headers, footers, notes, OCR errors like "eBAY" for "eBay"). Transaction types may be explicit (e.g., "Paid to" for debits, "Received from" for credits, "Debit"/"Credit" columns) or inferred from context/keywords (e.g., "Purchase" or "Withdrawal" implies debit; "Deposit" or "Refund" implies credit).

The input is raw, unstructured text from the entire PDF (all pages combined).

Perform extraction via chain-of-thought reasoning (document internally; output ONLY JSON):
1.  **Extract Metadata**: Scan for account_holder (e.g., name/email/phone like "ruchitdas36@gmail.com" or "Bit Manufacturing Ltd"; default "Unknown" if absent). account_number (e.g., "111-234-567-890", "12345678", or phone like "8433575939"; default "N/A"). period_start/end (e.g., "01 September 2025" → "09/01/2025"; infer from first/last transaction or "Issue Date" if missing; format as "MM/DD/YYYY"). When parsing numeric-only dates like '02/03/2025', assume the format is 'MM/DD/YYYY' unless the day value is greater than 12. beginning_balance (e.g., "Balance Brought Forward" or inferred from first balance; default 0.0). ending_balance (last balance or totals diff, e.g., Received - Sent; default 0.0). Normalize dates to "MM/DD/YYYY" strings; remove commas from floats (e.g., "8,313.30" → 8313.30).
2.  **Parse Transactions**: Identify all unique rows/blocks post-metadata (skip headers like "Date Transaction details Amount"). Mentally tabularize:
    - date (earliest field, e.g., "01 Sep, 2025 11:59 AM" → "09/01/2025"; include time if present).
    - description (concat text like "Paid to M S TIBBS FOODS PRIVATE LIMITED UPI ID: 524474349114 Paid by Axis Bank 9934").
    - Infer debit/credit: "Paid to/Sent/Out/Debit/Purchase/Withdrawal" → debit=amount, credit=0.0; "Received from/In/Credit/Deposit/Refund" → credit=amount, debit=0.0; column-based (e.g., "Paid Out" column); set missing to 0.0. Currency: Strip symbols (₹ → float).
    - balance: From explicit column (running total); if absent (e.g., UPI), set 0.0.
    - Handle formats: Aligned text (split by spaces); multi-line (group by date); lists (keyword-match). Dedupe; sort chronologically (earliest first).
3.  **Handle Errors and Warnings**: If you encounter a transaction line that is ambiguous or seems malformed (e.g., missing an amount), skip adding it to the `transactions` array. Instead, add a brief, descriptive string to the `warnings` array in the root of the final JSON object explaining what was skipped and why.

Few-shot examples (adapt for input):
Example 1 (Digital payment): Input: "Transaction statement period 01 September 2025 - 30 September 2025 Sent ₹8,844.85 Received ₹9,800 ... 01 Sep, 2025 11:59 AM Received from Ranjan Das ₹3,500" → Output: {{"account_holder": "ruchitdas36@gmail.com", "account_number": "8433575939", "period_start": "09/01/2025", "period_end": "09/30/2025", "beginning_balance": 0.0, "ending_balance": 0.0, "transactions": [{{"date": "09/01/2025", "description": "Received from Ranjan Das", "debit": 0.0, "credit": 3500.0, "balance": 0.0}}]}}
Example 2 (Traditional bank): Input: "Balance Brought Forward 8,313.30 ... mm/dd/yyyy Fast Payment Amazon 132.30 8,181.00" → Output: {{"account_holder": "Bit Manufacturing Ltd", "account_number": "111-234-567-890", "period_start": "mm/dd/yyyy", "period_end": "mm/dd/yyyy", "beginning_balance": 8313.30, "ending_balance": 5799.64, "transactions": [{{"date": "mm/dd/yyyy", "description": "Fast Payment Amazon", "debit": 132.30, "credit": 0.0, "balance": 8181.0}}]}}
Example 3 (Template/empty): Input: "Issue Date: mm/dd/yyyy Period: mm/dd/yyyy to mm/dd/yyyy" → Output: {{"account_holder": "Unknown", "account_number": "N/A", "period_start": "mm/dd/yyyy", "period_end": "mm/dd/yyyy", "beginning_balance": 0.0, "ending_balance": 0.0, "transactions": [], "warnings": ["Document appears to be a template with no transaction data."]}}

IMPORTANT: Do not invent or infer any data that is not explicitly present in the text. If a value like account_holder or a balance is missing, you MUST use the specified default values ("Unknown", "N/A", 0.0).

Full Input Text from all pages:
---
{full_document_text}
---

Output ONLY the valid JSON matching the schema. No text, explanations, or formatting.

JSON Schema:
{{
  "account_holder": "string",
  "account_number": "string",
  "period_start": "string",
  "period_end": "string",
  "beginning_balance": float,
  "ending_balance": float,
  "transactions": [
    {{
      "date": "string",
      "description": "string",
      "debit": float,
      "credit": float,
      "balance": float
    }}
  ],
  "warnings": [
      "string"
  ]
}}
"""
    
    print("Sending request to OpenRouter API with full document context...")

    # --- Step 3: Make the API Call ---
    response = client.chat.completions.create(
        extra_headers={
          "HTTP-Referer": "http://localhost",
          "X-Title": "IntelliStatement",
        },
        model="qwen/qwen-2.5-72b-instruct:free", # Using the specified powerful model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    
    print("Received response from OpenRouter API.")

    # --- Step 4: Validate and Return the Output ---
    extracted_json_string = response.choices[0].message.content
    validated_data = StatementData.model_validate_json(extracted_json_string)
    
    print("LLM output successfully validated against Pydantic schema.")
    return validated_data.model_dump()