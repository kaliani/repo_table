from fastapi import HTTPException
from app.core.db import conn, has_table
from app.core.llm import sql_chain, answer_chain, clean_sql

def run_chain(question: str) -> dict:
    if not has_table("reest"):
        raise HTTPException(status_code=409, detail="Table 'reest' not found. Upload a CSV/Excel first via /upload.")

    schema_str = conn.sql("DESCRIBE reest").df().to_string(index=False)
    sql_raw = sql_chain.invoke({"schema": schema_str, "question": question})
    sql_clean = clean_sql(sql_raw)

    try:
        res_df = conn.sql(sql_clean).df()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {e}\nSQL: {sql_clean}")

    context = res_df.head(200).to_string(index=False)
    final_answer = answer_chain.invoke({"context": context, "question": question})

    preview = res_df.head(50)
    return {
        "question": question,
        "sql": sql_clean,
        "total_rows": int(len(res_df)),
        "rows_preview": preview.to_dict(orient="records"),
        "answer": final_answer,
    }
