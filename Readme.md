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

### Configuration

1. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY="your_key_here"`
   - Other configuration parameters can be modified in `backend/core/config.py`

Note: If you used the `setup_project.bat` script, it will have prompted you to create the `.env` file and add your API key.

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