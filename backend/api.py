from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import time
import logging

# Import backend modules
from scraper import search_and_extract_content
from ai_integration import generate_ai_response
from export import export_to_pdf, export_to_json, export_to_txt, export_to_markdown, export_to_docx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Research Ninja API",
    description="API for AI-powered market research and competitor analysis",
    version="1.0.0")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request and response models
class ResearchQuery(BaseModel):
    query: str = Field(..., description="The research query to process")
    recency: str = Field("Past month",
                         description="Information recency filter")
    search_depth: int = Field(3, description="Search depth (1-10)")
    custom_urls: List[str] = Field(
        [], description="Additional URLs to include in research")
    ai_model: str = Field("GPT-4o mini",
                          description="AI model to use for analysis")


class ExportRequest(BaseModel):
    research_id: str = Field(...,
                             description="The ID of the research to export")
    format: str = Field(
        ..., description="Export format (PDF, JSON, TXT, Markdown, DOCX)")


class ResearchResponse(BaseModel):
    research_id: str
    query: str
    response: str
    sources: List[Dict[str, Any]]
    timestamp: str


class ExportResponse(BaseModel):
    research_id: str
    format: str
    content: str
    timestamp: str


# In-memory store for research results
research_store = {}


@app.get("/")
def root():
    return {"message": "Welcome to the Research Ninja API"}


@app.post("/research", response_model=ResearchResponse)
async def create_research(research_query: ResearchQuery):
    try:
        research_id = f"research_{int(time.time())}"
        search_results = search_and_extract_content(
            query=research_query.query,
            recency=research_query.recency,
            search_depth=research_query.search_depth,
            custom_urls=research_query.custom_urls)
        response, formatted_sources = generate_ai_response(
            query=research_query.query,
            search_results=search_results,
            model=research_query.ai_model)
        research_data = {
            "research_id": research_id,
            "query": research_query.query,
            "response": response,
            "sources": formatted_sources,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        research_store[research_id] = research_data
        return research_data
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")


@app.get("/research/{research_id}", response_model=ResearchResponse)
async def get_research(research_id: str):
    research_data = research_store.get(research_id)
    if not research_data:
        raise HTTPException(status_code=404, detail="Research not found")
    return research_data


@app.post("/export", response_model=ExportResponse)
async def export_research(export_request: ExportRequest):
    research_data = research_store.get(export_request.research_id)
    if not research_data:
        raise HTTPException(status_code=404, detail="Research not found")
    export_functions = {
        "PDF": export_to_pdf,
        "JSON": export_to_json,
        "TXT": export_to_txt,
        "MARKDOWN": export_to_markdown,
        "DOCX": export_to_docx
    }
    export_func = export_functions.get(export_request.format.upper())
    if not export_func:
        raise HTTPException(status_code=400,
                            detail="Unsupported export format")
    content = export_func(research_data)
    return {
        "research_id": export_request.research_id,
        "format": export_request.format,
        "content": content,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }


@app.get("/formats")
def get_supported_formats():
    return ["PDF", "JSON", "TXT", "MARKDOWN", "DOCX"]


@app.get("/batch-export/{research_id}")
async def batch_export(research_id: str, formats: str = Query(None)):
    research_data = research_store.get(research_id)
    if not research_data:
        raise HTTPException(status_code=404, detail="Research not found")
    requested_formats = formats.upper().split(",") if formats else [
        "PDF", "JSON", "TXT", "MARKDOWN", "DOCX"
    ]
    results = {}
    for fmt in requested_formats:
        if fmt in ["PDF", "JSON", "TXT", "MARKDOWN", "DOCX"]:
            results[fmt] = globals()[f"export_to_{fmt.lower()}"](research_data)
    return results


@app.get("/models", response_model=List[str])
async def get_available_models():
    return ["GPT-4o mini", "Gemini", "Claude", "Cohere"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
