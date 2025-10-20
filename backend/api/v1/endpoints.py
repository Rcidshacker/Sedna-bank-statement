# --- Imports ---
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

# --- MODIFIED IMPORT ---
from ...processing_pipeline.a_structuring import structure_document_by_page
from ...processing_pipeline.b_extraction import extract_data_with_llm
from ...processing_pipeline.c_validation import validate_and_enrich_data
from ...utils.file_handler import save_temp_file
from ...database.database import get_db
from ...database import crud
from ...core.models import StatementData

router = APIRouter()

@router.post("/parse")
async def parse_statement(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_file_path = save_temp_file(file)
    
    try:
        # --- MODIFIED FUNCTION CALL ---
        page_texts = structure_document_by_page(temp_file_path)
        
        extracted_data_dict = extract_data_with_llm(page_texts)
        
        pydantic_data = StatementData(**extracted_data_dict)
        crud.save_statement_data(db=db, data=pydantic_data, filename=file.filename)
        
        final_data_for_frontend = validate_and_enrich_data(extracted_data_dict)
        
        return final_data_for_frontend

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred during document processing: {e}"
        )
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")