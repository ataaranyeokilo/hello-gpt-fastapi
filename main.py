from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import azure_client  # ⬅️ changed: import module, not symbol

app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest):
    try:
        answer = azure_client.ask_gpt(request.question)  # ⬅️ changed call site
        return {"answer": answer}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))