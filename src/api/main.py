from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from src.core.workflow import run_workflow
from src.core.state import SupportState
import logging
import yaml
from pathlib import Path


# Load configuration
config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=config.get("log_file", "logs/main_log.log"),
    filemode='a'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Support AI",
    description="A multi-agent customer support system powered by LangGraph.",
    version="1.0.0"
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


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    """Serve the HTML form page"""
    logger.info("Loaded index.html")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, query: str = Form(...)):
    """Process the form submission and return HTML response"""
    try:
        logger.info(f"Processing form query: {query}")
        result = run_workflow(query)
        
        # Convert the result to a displayable format
        response_data = {
            "request": request,
            "result": result,
            "message": "Query processed successfully",
            "status": "success"
        }
        
        return templates.TemplateResponse("index.html", response_data)
    except Exception as e:
        logger.error(f"Error processing query '{query}: {str(e)}'")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e),
            "status": "error"
        })


# Endpoints
@app.post("/", response_model=QueryResponse)
async def process_single_query(request: QueryRequest):
    """
    Process a single customer query through the support workflow.
    
    Args:
        request: QueryRequest with a single query string.
    
    Returns:
        QueryResponse with the processed state and a success message.
    """
    try:
        logger.info(f"Processing single query: {request.query}")
        result = run_workflow(request.query)
        return QueryResponse(state=result, message="Query processed successfully")
    except Exception as e:
        logger.error(f"Error processing query '{request.query}: {str(e)}'")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "timestamp": str(Path(config["log_file"]).stat().st_mtime)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)