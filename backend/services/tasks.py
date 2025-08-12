import json, time, os
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
        "event": "ask",
        "question": question,
        "sql": sql,
        "total_rows": total_rows,
    })

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
            "event": "post_upload_profile",
            "summary": summary,
        })
    except Exception as e:
        _append_log({
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": "post_upload_profile_error",
            "error": str(e),
        })
