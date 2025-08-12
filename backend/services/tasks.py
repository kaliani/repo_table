# services/tasks.py
import json, os
from datetime import datetime, timezone
from app.core.db import conn  

LOG_PATH = os.getenv("APP_LOG_PATH", "logs/events.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def _append_log(payload: dict):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def log_ask_event(question: str, sql: str, total_rows: int):
    _append_log({
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": "info",
        "event": "ask",
        "question": question,
        "sql": sql,
        "total_rows": total_rows,
    })

def log_error(event: str, question: str, error: str,
              sql: str | None = None,
              phase: str | None = None,
              status: int | None = None,
              extra: dict | None = None):
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": "error",
        "event": event,            
        "phase": phase,     
        "status": status,       
        "question": question,
        "sql": sql,
        "error": error,
    }
    if extra:
        payload["extra"] = extra
    _append_log(payload)

def post_upload_profile():
    try:
        df = conn.sql("SELECT * FROM reest").df()
        summary = {
            "rows": len(df),
            "cols": list(map(str, df.columns)),
            "nulls": {c: int(df[c].isna().sum()) for c in df.columns},
        }
        _append_log({
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": "info",
            "event": "post_upload_profile",
            "summary": summary,
        })
    except Exception as e:
        log_error(event="post_upload_profile_error", question="", error=str(e))