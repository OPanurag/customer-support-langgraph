# app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from src.langie.pipeline import LangGraphAgent
import uvicorn

app = FastAPI(title="LangGraph Customer Support API")

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize LangGraph pipeline once
AGENT = LangGraphAgent(config_path="config/stages.yaml")

@app.get("/")
def index():
    """Serve frontend HTML."""
    return FileResponse("static/index.html")

@app.post("/run_pipeline")
async def run_pipeline(request: Request):
    """Endpoint to run LangGraph pipeline."""
    payload = await request.json()
    try:
        response = AGENT.run(payload)
        return JSONResponse(response)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
