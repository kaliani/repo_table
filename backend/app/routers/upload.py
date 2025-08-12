import io, pandas as pd
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..core.config import settings
from ..core.db import conn

router = APIRouter()

def _detect_fmt(filename: str) -> str:
    ext = (filename or "").lower().rsplit(".", 1)[-1]
    if ext == "csv": return "csv"
    if ext in ("xlsx", "xls"): return "excel"
    return ""

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    fmt: Optional[str] = Form(None),
    sheet_name: Optional[str] = Form(None),
    sep: Optional[str] = Form(None),
    encoding: Optional[str] = Form(None),
):
    fmt = (fmt or _detect_fmt(file.filename)).lower()
    if fmt not in settings.ALLOWED_FORMATS:
        raise HTTPException(status_code=415, detail=f"Unsupported format: {fmt}. Allowed: {sorted(settings.ALLOWED_FORMATS)}")

    data = await file.read()
    buf = io.BytesIO(data)

    try:
        if fmt == "csv":
            read_kwargs = {}
            if sep: read_kwargs["sep"] = sep
            if encoding: read_kwargs["encoding"] = encoding
            df = pd.read_csv(buf, **read_kwargs)
        else:
            df = pd.read_excel(buf, sheet_name=sheet_name if sheet_name else 0)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse {fmt}: {e}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file produced an empty dataframe.")

    try:
        conn.execute("DROP TABLE IF EXISTS reest")
        conn.register("tmp_df", df)
        conn.execute("CREATE TABLE reest AS SELECT * FROM tmp_df")
        conn.unregister("tmp_df")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DuckDB load error: {e}")

    return {"ok": True, "rows": int(len(df)), "columns": list(map(str, df.columns)), "format": fmt}
