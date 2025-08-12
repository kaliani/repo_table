from fastapi import APIRouter
from schemas import AskRequest
from services.qa_service import run_chain

router = APIRouter()

@router.post("/ask")
def ask(req: AskRequest):
    return run_chain(req.question)
