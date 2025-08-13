# LLM Q&A 
```
repo_table/
├── backend/ # FastAPI service
├── frontend/ # Frontend with streamlit
├── data/ # Example datasets (if any)
├── requirements.txt # Python dependencies
└── README.md
```
## Installation & Setup

### Clone the repository
```
git clone https://github.com/kaliani/repo_table.git
cd repo_table

### Create new env
python3 -m venv my_env
source my_env/bin/activate  

### Install new env
pip install -r requirements.txt
```


##  Environment Variables
```Create a .env file inside the backend directory:
OPENAI_API_KEY=sk-...
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=pr-gripping-vibration-83
LANGSMITH_API_KEY=lsv2-...
OPENAI_MODEL=gpt-4o
```

Description:

- OPENAI_API_KEY – Your OpenAI API key.

- OPENAI_MODEL – The main LLM model (gpt-4o used in this project).

- LANGSMITH_* – LangSmith tracing configuration for monitoring and debugging.


## Running the Application
You need two terminal windows — one for the backend, one for the frontend.


### Start the Backend (FastAPI)
```
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start the Frontend (Streamlit)
```
cd frontend
streamlit run streamlit_app.py
```

[[Watch the demo]](https://share.descript.com/view/RYoxyllEZJD)
