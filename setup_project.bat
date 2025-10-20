@echo off
setlocal
cls

echo.
echo  ======================================================
echo   IntelliStatement Project Scaffolding & Setup Script
echo  ======================================================
echo.
echo  This script will create the project structure and
echo  install all required Python libraries.
echo.
echo  IMPORTANT: Please ensure you are running this from
echo  an ACTIVE virtual environment.
echo.
pause
cls

echo [PHASE 1 of 3] Creating project directories...
echo.

mkdir backend
mkdir backend\api
mkdir backend\api\v1
mkdir backend\core
mkdir backend\processing_pipeline
mkdir backend\utils
mkdir frontend

echo   - backend/
echo   - backend/api/v1/
echo   - backend/core/
echo   - backend/processing_pipeline/
echo   - backend/utils/
echo   - frontend/
echo.
echo Directories created successfully.
echo.
pause
cls

echo [PHASE 2 of 3] Creating empty Python files...
echo.

:: Create backend files
type nul > backend\main.py
type nul > backend\api\v1\endpoints.py
type nul > backend\core\config.py
type nul > backend\core\models.py
type nul > backend\processing_pipeline\__init__.py
type nul > backend\processing_pipeline\a_structuring.py
type nul > backend\processing_pipeline\b_extraction.py
type nul > backend\processing_pipeline\c_validation.py
type nul > backend\utils\file_handler.py

:: Create frontend file
type nul > frontend\frontend_app.py

echo   - Created all necessary .py files.
echo.
echo Project files created successfully.
echo.
pause
cls

echo [PHASE 3 of 3] Creating requirements.txt and installing libraries...
echo.

:: Create the requirements.txt file
echo fastapi > requirements.txt
echo uvicorn[standard] >> requirements.txt
echo pydantic >> requirements.txt
echo python-dotenv >> requirements.txt
echo unstructured[pdf] >> requirements.txt
echo openai >> requirements.txt
echo pandas >> requirements.txt
echo numpy >> requirements.txt
echo lxml >> requirements.txt
echo streamlit >> requirements.txt
echo altair >> requirements.txt
echo pdf2image >> requirements.txt
echo opencv-python >> requirements.txt
echo google-cloud-vision >> requirements.txt

echo requirements.txt file has been created.
echo.
echo Now installing libraries. This may take several minutes...
echo.

:: Install the libraries using pip
pip install -r requirements.txt

echo.
echo  ======================================================
echo   Project setup is complete!
echo  ======================================================
echo.
echo  Next Steps:
echo    1. Create a file named '.env' in the root folder.
echo    2. Add your OpenAI API key to it: OPENAI_API_KEY="your_key_here"
echo    3. Start coding!
echo.

endlocal
pause