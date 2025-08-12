from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .core.config import settings
from .core.db import load_csv_to_reest
from .routers import health, upload, qa

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
