from fastapi import APIRouter, BackgroundTasks
from fastapi import APIRouter
from schemas import AskRequest
from services.qa_service import run_chain
from services.tasks import log_ask_event

router = APIRouter()

@router.post("/ask")
def ask(req: AskRequest, background_tasks: BackgroundTasks):
    result = run_chain(req.question)
    background_tasks.add_task(
        log_ask_event,
        req.question,
        result.get("sql", ""),
        result.get("total_rows", 0),
    )
    return result