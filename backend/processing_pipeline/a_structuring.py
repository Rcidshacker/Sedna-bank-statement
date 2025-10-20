# --- Imports ---
import os
import uuid
import mimetypes
from pathlib import Path
from collections import defaultdict
from PIL import Image
import cv2
import numpy as np
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.image import partition_image
from unstructured.partition.auto import partition

# --- Helper for Preprocessing ---
def preprocess_image(image_path: str) -> str:
    """Applies basic preprocessing (grayscale, thresholding) to an image."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save to a unique temporary file to avoid conflicts
    preprocessed_path = f"temp_uploads/preprocessed_{uuid.uuid4()}.jpg"
    cv2.imwrite(preprocessed_path, thresh)
    return preprocessed_path

# --- Core Function ---
def structure_document_by_page(file_path: str) -> list[dict]:
    """
    Enhanced dispatcher: Detects type via ext + MIME, preprocesses images, and returns enriched page data.
    """
    print(f"Structuring document: {file_path}")
    path = Path(file_path)
    file_ext = path.suffix.lower()
    mime_type, _ = mimetypes.guess_type(file_path)
    
    elements = []
    temp_files_to_clean = []

    try:
        if file_ext == ".pdf" or mime_type == "application/pdf":
            print("PDF detected. Using partition_pdf.")
            elements = partition_pdf(filename=file_path, strategy="hi_res", infer_table_structure=True)
        
        elif file_ext in [".png", ".jpg", ".jpeg"] or (mime_type and mime_type.startswith("image/")):
            print("Image detected. Preprocessing and using partition_image.")
            preprocessed_path = preprocess_image(file_path)
            temp_files_to_clean.append(preprocessed_path)
            elements = partition_image(filename=preprocessed_path, strategy="hi_res")

        else:
            print(f"Unknown type ({file_ext}/{mime_type}). Falling back to auto-partition.")
            elements = partition(filename=file_path, strategy="hi_res")

        # Group elements by page number
        pages_data = defaultdict(list)
        for el in elements:
            page_num = el.metadata.page_number or 1
            pages_data[page_num].append(el.text)

        # Combine text for each page
        page_outputs = []
        for page_num in sorted(pages_data.keys()):
            full_text = "\n\n".join(pages_data[page_num])
            page_outputs.append({"page": page_num, "text": full_text})
        
        print(f"Structuring complete: {len(page_outputs)} pages found.")
        return page_outputs

    finally:
        # Clean up any temporary preprocessed images
        for temp_file in temp_files_to_clean:
            if os.path.exists(temp_file):
                os.remove(temp_file)