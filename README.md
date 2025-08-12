# 📚 LLM Q&A App with Feedback

This application allows you to ask questions to an LLM via a **FastAPI** backend and receive answers with the option to rate them (**like/dislike**).  
It also supports uploading CSV/Excel files to the backend for further analysis.

---

## Requirements

Before running, make sure you have:
- Python **3.9+**
- `pip` (Python package manager)
- A running **FastAPI backend** with these endpoints:
  - `GET /health` — health check
  - `POST /ask` — send a question to the LLM
  - `POST /upload` — upload data
  - *(optional)* `POST /save_feedback` — store likes/dislikes

---

## Installation

```bash
# Clone the repository
git https://github.com/kaliani/repo_table.git
cd repo_table

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt


1. Start the FastAPI backend:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

2. Start the Streamlit frontend:
streamlit run streamlit_app.py

3. Open in your browser:
http://localhost:8501
