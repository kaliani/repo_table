import os, re, duckdb, pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CSV_PATH = os.getenv("REEST_CSV_PATH", "data/reest.csv")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

CSV_PATH = os.path.abspath(CSV_PATH)  # важливо для uvicorn робочого каталогу

conn = duckdb.connect(database=":memory:")
conn.sql(f"CREATE TABLE reest AS SELECT * FROM read_csv_auto('{CSV_PATH}')")

llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, api_key=OPENAI_API_KEY)

def clean_sql(s: str) -> str:
    s = re.sub(r"```(?:sql)?\s*", "", s, flags=re.IGNORECASE)
    s = s.replace("```", "")
    return s.strip().split(";")[0].strip()

sql_prompt = PromptTemplate.from_template("""
Given the following table schema for the table `reest`:

{schema}

Write an SQL statement to answer the following question:

{question}

Provide all rows from the table (select *) when relevant.
Provide a LIMIT where applicable.
Respond with only the SQL statement.
""")
sql_chain = sql_prompt | llm | StrOutputParser()

answer_chain = PromptTemplate.from_template("""
Use the following data to provide a definitive answer to the user's question:

{context}

The question is: {question}
""") | llm | StrOutputParser()

def run_chain(question: str):
    # ✅ ВАЖЛИВО: тільки conn.sql(...)
    schema_str = conn.sql("DESCRIBE reest").df().to_string(index=False)

    sql_raw = sql_chain.invoke({"schema": schema_str, "question": question})
    sql_clean = clean_sql(sql_raw)

    try:
        res_df = conn.sql(sql_clean).df()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {e}\nSQL: {sql_clean}")

    context = res_df.head(200).to_string(index=False)
    final_answer = answer_chain.invoke({"context": context, "question": question})

    return {
        "question": question,
        "sql": sql_clean,
        "total_rows": int(len(res_df)),
        "rows_preview": res_df.head(50).to_dict(orient="records"),
        "answer": final_answer,
    }

app = FastAPI(title="DuckDB LLM QA", version="1.0.0")

# Опційно гарантуємо, що таблиця є при рестарті з іншого CWD
@app.on_event("startup")
def ensure_table():
    try:
        conn.sql("SELECT 1 FROM reest LIMIT 1")
    except duckdb.CatalogException:
        conn.sql(f"CREATE TABLE reest AS SELECT * FROM read_csv_auto('{CSV_PATH}')")

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    # Простий sanity-check
    n = conn.sql("SELECT COUNT(*) AS n FROM reest").df().iloc[0,0]
    return {"ok": True, "rows": int(n)}

@app.post("/ask")
def ask(req: AskRequest):
    return run_chain(req.question)
