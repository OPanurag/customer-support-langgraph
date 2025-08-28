# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pipeline.abilities.knowledge_base_search import KnowledgeBaseSearch

app = FastAPI()

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load pipeline components
kb_search = KnowledgeBaseSearch(config={
    "db_path": "data/chroma",
    "collection": "faq",
    "top_k": 3
})

class ChatPayload(BaseModel):
    customer_name: str
    email: str
    query: str

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return f.read()

@app.post("/chat")
async def chat(payload: ChatPayload):
    # Build state for pipeline
    state = {
        "input": {"text": payload.query},
        "customer_name": payload.customer_name,
        "email": payload.email
    }

    # Run KB search
    state = kb_search.run(state)

    # Extract top answer if available
    kb_results = state.get("knowledge_base", [])
    if kb_results:
        main_answer = kb_results[0].get("answer", "No answer found")
    else:
        main_answer = "Sorry, I couldn’t find an answer to your query."

    # Build response JSON
    return JSONResponse({
        "customer": payload.customer_name,
        "query": payload.query,
        "response": main_answer,
        "alternatives": [
            {
                "question": r.get("question"),
                "answer": r.get("answer"),
                "doc": r.get("doc")
            }
            for r in kb_results
        ]
    })
