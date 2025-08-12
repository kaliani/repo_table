# LLM Q&A 

## ⚙️ Features
- **Natural language to SQL** query generation.
- **Powered by OpenAI GPT-4o** as the primary LLM.
- **LangSmith tracing** for monitoring and debugging responses.
- **Like/Dislike feedback** for rating LLM answers.
- **Extended logging** for capturing failed requests, LLM errors (e.g., HTTP 500), and other unexpected issues.
- Upload and process **CSV** or **Excel** files.
- Optional format, sheet name, and CSV separator/encoding controls.


repo_table/
│
├── backend/          # FastAPI application
├── frontend/         # Streamlit application
├── data/             # Example datasets (if any)
├── requirements.txt  # Python dependencies
└── README.md


---

## Installation & Setup

### Clone the repository
```bash
git clone https://github.com/kaliani/repo_table.git
cd repo_table

### Clone the repository
python3 -m venv my_env
source my_env/bin/activate   # On Linux/Mac
my_env\Scripts\activate      # On Windows

### Clone the repository
pip install -r requirements.txt


##  Environment Variables
Create a .env file inside the backend directory:
OPENAI_API_KEY=sk-...
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=pr-gripping-vibration-83
LANGSMITH_API_KEY=lsv2-...
OPENAI_MODEL=gpt-4o

Description:
OPENAI_API_KEY – Your OpenAI API key.

OPENAI_MODEL – The main LLM model (gpt-4o used in this project).

LANGSMITH_* – LangSmith tracing configuration for monitoring and debugging.


## Running the Application
You need two terminal windows — one for the backend, one for the frontend.


### Start the Backend (FastAPI)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### Start the Frontend (Streamlit)
cd frontend
streamlit run streamlit_app.py
