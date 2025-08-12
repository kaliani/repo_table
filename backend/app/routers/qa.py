from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.schemas import AskRequest
from services.qa_service import run_chain
from services.tasks import log_ask_event, log_error

router = APIRouter()

@router.post("/ask")
def ask(req: AskRequest, background_tasks: BackgroundTasks):
    try:
        result = run_chain(req.question)

        if result.get("warning"):
            background_tasks.add_task(
                log_error,
                "ask_fallback",
                req.question,
                result.get("error", "unknown"),
                sql=result.get("sql"),
                phase="fallback",
                status=200,
            )
        else:
            background_tasks.add_task(
                log_ask_event,
                req.question,
                result.get("sql", ""),
                result.get("total_rows", 0),
            )
        return result

    except HTTPException as e:
        background_tasks.add_task(
            log_error,
            "http_exception",
            req.question,
            f"{e.status_code}: {e.detail}",
            status=e.status_code,
        )
        return JSONResponse(status_code=200)

    except Exception as e:
        background_tasks.add_task(
            log_error,
            "unhandled_exception",
            req.question,
            str(e),
            status=500,
        )
        return JSONResponse(status_code=200)
