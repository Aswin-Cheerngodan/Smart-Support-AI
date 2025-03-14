from fastapi import FastAPI, HTTPException
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
    filename=config.get("log_file", "logs/api.log")
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Support AI",
    description="A multi-agent customer support system powered by LangGraph.",
    version="1.0.0"
)

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    query: str

class BatchQueryRequest(BaseModel):
    queries: List[str]

class QueryResponse(BaseModel):
    state: SupportState
    message: str

# Endpoints
@app.post("/support/query", response_model=QueryResponse)
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
    uvicorn.run(app, host="0.0.0.0", port=8000)