from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from contextlib import asynccontextmanager
from .core.config import settings
from .core.db import load_csv_to_reest
from .routers import health, upload, qa
from services.tasks import log_error

app = FastAPI(title="local qa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_csv_to_reest()
    yield

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(qa.router)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    try:
        body = await request.json()
        question = body.get("question", "")
    except Exception:
        question = ""
    log_error("global_unhandled_exception", question, f"{type(exc).__name__}: {exc}", status=500)
    return JSONResponse(
        status_code=200,
        content={
            "warning": "FALLBACK_ANSWER",
            "error": f"UNHANDLED_EXCEPTION: {type(exc).__name__}: {exc}",
            "answer": "I was not able to generate a valid answer for this query.",
            "sql": None,
            "rows_preview": [],
            "total_rows": 0,
            "question": question,
        },
    )