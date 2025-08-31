from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure_client import ask_gpt




# Init FastAPI app
app = FastAPI()

# Request model
class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: AskRequest):
    try:
        answer = ask_gpt(request.question)
        return {"answer": answer}
    except RuntimeError as e:
        # Surface a clean message to the client; log details already handled in azure_client
        raise HTTPException(status_code=503, detail=str(e))