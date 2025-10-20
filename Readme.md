# IntelliStatement: Intelligent Bank Statement Analyzer

## Overview

IntelliStatement is a sophisticated bank statement analysis tool that combines modern web technologies with artificial intelligence to automatically process, extract, and analyze data from bank statements in various formats (PDF/images). The system provides an intuitive web interface for users to upload their statements and gain valuable insights into their financial data.

## Features

- 📄 PDF and Image Processing
- 🤖 AI-Powered Data Extraction
- 📊 Interactive Data Visualization
- 💾 Secure Data Storage
- 🔄 Real-time Processing
- 📱 Responsive Web Interface

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy
- **AI/ML**: OpenAI API (via OpenRouter)
- **Data Processing**: Python with various data processing libraries

### Frontend
- **Framework**: Streamlit
- **Visualization**: Altair
- **Data Handling**: Pandas

## Project Structure

```
├── backend/                 # FastAPI Backend
│   ├── api/                # API endpoints
│   ├── core/              # Core configuration and models
│   ├── database/          # Database models and CRUD operations
│   ├── processing_pipeline/# Data processing modules
│   └── utils/             # Utility functions
├── frontend/              # Streamlit Frontend
└── temp_uploads/         # Temporary storage for uploads
```

## Getting Started

### Prerequisites

1. Python 3.13 or higher
2. Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rcidshacker/Sedna-bank-statement.git
cd Sedna-bank-statement
```

2. Set up the virtual environment:
```bash
python -m venv statement
statement\Scripts\activate  # On Windows
# source statement/bin/activate  # On Unix/MacOS
```

3. Automated Setup (Recommended):
```bash
setup_project.bat
```
This script will:
- Create all necessary project directories
- Set up empty Python files with correct structure
- Create and populate requirements.txt
- Install all required dependencies automatically

4. Manual Installation (Alternative):
If you prefer manual installation, you can install dependencies directly:
```bash
pip install -r requirements.txt
```

Required Dependencies:
- fastapi
- uvicorn[standard]
- pydantic
- python-dotenv
- unstructured[pdf]
- openai
- pandas
- numpy
- lxml
- streamlit
- altair
- pdf2image
- opencv-python
- google-cloud-vision

### Environment Configuration

1. Environment Files:
   - `.env.example`: Template file showing required environment variables
   - `.env`: Your actual environment file (needs to be created, not version controlled)

2. Setting up your environment:
   ```bash
   # 1. Copy the example file
   cp .env.example .env
   
   # 2. Edit .env file and add your actual API key
   OPENAI_API_KEY="your_actual_key_here"
   ```

### Project Structure Details

```
backend/
├── api/
│   └── v1/
│       └── endpoints.py          # FastAPI route definitions and API endpoints
├── core/
│   ├── config.py                # Application configuration and env management
│   └── models.py                # Core data models and Pydantic schemas
├── database/
│   ├── models.py                # SQLAlchemy database models
│   ├── database.py              # Database connection and session management
│   └── crud.py                  # Database CRUD operations
├── processing_pipeline/
│   ├── a_structuring.py         # Document preprocessing and structuring
│   ├── b_extraction.py          # LLM-based data extraction
│   └── c_validation.py          # Data validation and error checking
├── utils/
│   └── file_handler.py          # File upload and management utilities
└── main.py                      # FastAPI application entry point

frontend/
└── frontend_app.py              # Streamlit web interface
```

### Key Components

1. **Database Layer** (`backend/database/`):
   - `models.py`: Database schema definitions
     - `Statement`: Stores bank statement metadata
     - `Transaction`: Stores individual transactions
   - `database.py`: Database connection management
     - SQLite configuration
     - Session management
     - Connection pooling
   - `crud.py`: Database operations
     - Statement creation/retrieval
     - Transaction management
     - Data persistence logic
   - `__init__.py`: Package initialization

2. **Configuration** (`backend/core/`):
   - `config.py`: Environment and settings management
     - Environment variable handling
     - Application settings
     - Pydantic-based configuration
   - `models.py`: Pydantic models for data validation

3. **Processing Pipeline** (`backend/processing_pipeline/`):
   - `a_structuring.py`: Document preprocessing
     - PDF/Image parsing
     - Text extraction
     - Layout analysis
   - `b_extraction.py`: Data extraction
     - OpenAI API integration
     - Pattern recognition
     - Data structuring
   - `c_validation.py`: Data validation
     - Format verification
     - Data consistency checks
     - Error handling
   - `__init__.py`: Pipeline initialization

4. **API Layer** (`backend/api/v1/`):
   - `endpoints.py`: REST API endpoints
     - File upload handling
     - Processing status tracking
     - Data retrieval methods
     - Error handling

5. **Utility Functions** (`backend/utils/`):
   - `file_handler.py`: File management
     - Temporary file storage
     - File upload processing
     - Clean-up routines
     - UUID-based file naming

6. **Frontend Application** (`frontend/`):
   - `frontend_app.py`: Streamlit interface
     - User interface components
     - File upload functionality
     - Data visualization
     - Interactive analysis features

7. **Project Root**:
   - `main.py`: FastAPI application entry point
   - `requirements.txt`: Project dependencies
   - `.env.example`: Environment template
   - `.env`: Local environment configuration
   - `setup_project.bat`: Automated setup script
   - `.gitignore`: Git exclusion patterns

8. **Data Storage**:
   - `temp_uploads/`: Temporary file storage
   - `intellistatement.db`: SQLite database file (created on first run)

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend application:
```bash
cd frontend
streamlit run frontend_app.py
```

3. Access the application at `http://localhost:8501`

## Usage

1. Open the web interface
2. Upload your bank statement (PDF/Image)
3. Wait for the AI-powered processing
4. View and analyze the extracted data
5. Export or save the results as needed

## Features in Detail

### Data Processing Pipeline

1. **Structuring** (`a_structuring.py`):
   - Document preprocessing
   - Layout analysis
   - Text extraction

2. **Extraction** (`b_extraction.py`):
   - AI-powered data extraction
   - Pattern recognition
   - Context understanding

3. **Validation** (`c_validation.py`):
   - Data validation
   - Error checking
   - Format standardization

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the powerful LLM capabilities
- FastAPI for the efficient backend framework
- Streamlit for the intuitive frontend development

---

For more information or support, please open an issue in the repository.