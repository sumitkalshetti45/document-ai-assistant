from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import generate_response
from app.graph_setup import graph
from app.rag_setup import setup_chroma

app = FastAPI()
vectorstore = None

class ChatRequest(BaseModel):
    user_query: str

@app.on_event("startup")
async def startup_event():
    global vectorstore
    vectorstore = setup_chroma(["data/sample.txt"])

@app.post("/chat")
async def chat(request: ChatRequest):
    global vectorstore
    graph.transition("ask_question")
    response = generate_response(request.user_query, vectorstore)
    graph.transition("answer_question")
    return {"response": response}