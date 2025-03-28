from fastapi import FastAPI, HTTPException, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from src.core.workflow import run_workflow
from src.agents.categorizer_agent import categorizer
from src.core.state import SupportState
import logging
import yaml
from pathlib import Path
from src.utils.logger import setup_logger

# Load configuration
config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

logger = setup_logger(__name__, "logs/app.log")

# Initialize FastAPI app
app = FastAPI(
    title="Smart Support AI",
    description="A multi-agent customer support system powered by LangGraph.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8000"],  # Add frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Set up templates
templates = Jinja2Templates(directory="src/api/templates")

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    query: str

class BatchQueryRequest(BaseModel):
    queries: List[str]

class QueryResponse(BaseModel):
    state: SupportState
    message: str

# Serve HTML form (optional)
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """Serve the HTML form page"""
    logger.info("Loaded index.html")
    return templates.TemplateResponse("index.html", {"request": request})

# Process query from frontend
@app.post("/process-query")
async def process_query_endpoint(request: QueryRequest):
    """Process a single customer query and return JSON response for the frontend."""
    try:
        logger.info(f"Processing query: {request.query}")
        state = SupportState({"query": request.query})  # Create state object
        updated_state = categorizer(state)  # Run categorization
        result = updated_state['category']  # Get the category
        response = result  # Format response
        return {"response": response}  # Match frontend expectation
    except Exception as e:
        logger.error(f"Error processing query '{request.query}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Optional: Handle root endpoint to avoid 405
@app.get("/")
async def root():
    """Redirect or provide a simple message for the root URL."""
    return {"message": "Welcome to Smart Support AI. Use /home for the UI or /process-query for API."}

# Health check
@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "timestamp": str(Path(config["log_file"]).stat().st_mtime)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)