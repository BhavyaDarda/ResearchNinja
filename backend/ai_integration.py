import os
import json
import time
import logging
import requests
import re
from typing import List, Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT_TEMPLATE = """You are Research Ninja, an AI-powered content research platform that provides comprehensive market analysis.
Your task is to analyze the provided information and generate a detailed research report.
Structure your response in clearly outlined sections with actionable insights and source citations."""
  
def generate_ai_response(query: str, search_results: List[Dict[str, Any]], model: str = "Gemini") -> Tuple[str, List[Dict[str, Any]]]:
    """
    Generate an AI response based on search results.
    """
    formatted_sources = [
        {"id": i + 1, "title": r.get("title", "No Title"), "url": r.get("url", ""), "accessed_date": r.get("accessed_date", "")}
        for i, r in enumerate(search_results)
    ]
    logger.info("Formatted sources: %s", json.dumps(formatted_sources, indent=2))
    
    valid_results = [r for r in search_results if r.get("content")]
    if not valid_results:
        logger.warning("No valid content in search results.")
        return _generate_dummy_response(query, formatted_sources), formatted_sources
    
    if model == "Gemini":
        response = _generate_response_gemini(query, valid_results, formatted_sources)
    elif model == "Cohere":
        response = _generate_response_cohere(query, valid_results, formatted_sources)
    else:
        response = _generate_response_gemini(query, valid_results, formatted_sources)
    
    if formatted_sources and not any(f"[{i+1}]" in response for i in range(len(formatted_sources))):
        response += "\n\n## Sources\n" + "\n".join(f"{src['id']}. [{src['title']}]({src['url']})" for src in formatted_sources)
    return response, formatted_sources

def _prepare_context(categorized_results: Dict[str, List[Dict[str, Any]]]) -> str:
    context = ""
    source_mapping = {}
    source_index = 1

    for category, results in categorized_results.items():
        context += f"## {category.upper()} INFORMATION\n\n"
        for result in results:
            if result.get("url") in source_mapping:
                continue
            source_mapping[result["url"]] = source_index
            snippet = result.get("content", "")[:3000] + ("..." if len(result.get("content", "")) > 3000 else "")
            context += f"Source [{source_index}]: {result.get('title', 'No Title')}\nURL: {result.get('url')}\nContent: {snippet}\n\n"
            source_index += 1
    return context

# Gemini API integration
def _generate_response_gemini(query: str, search_results: List[Dict[str, Any]], formatted_sources: List[Dict[str, Any]]) -> str:
    api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("Missing Gemini API key.")
        return "Gemini API key missing. Please set it in settings."
    context = _prepare_context({"gemini": search_results})
    prompt = f"Research Query: {query}\n\nSources:\n{context}\n\nProvide comprehensive analysis."
    try:
        # Pass the API key as a query parameter only (remove Authorization header)
        response_post = requests.post(
            "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": api_key},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4000}
            },
            timeout=60
        )
        response_post.raise_for_status()
        result_json = response_post.json()
        return result_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logger.error("Gemini API error: %s", str(e))
        return f"Gemini API error: {str(e)}. Please verify your GEMINI_API_KEY and its permissions."

# Cohere API integration with retry mechanism and increased timeout
def _generate_response_cohere(query: str, search_results: List[Dict[str, Any]], formatted_sources: List[Dict[str, Any]] = None) -> str:
    api_key: Optional[str] = os.getenv("COHERE_API_KEY")
    if not api_key:
        logger.warning("Missing Cohere API key.")
        return "Cohere API key missing. Please set it in settings."
    context = _prepare_context({"cohere": search_results})
    prompt = f"{SYSTEM_PROMPT_TEMPLATE}\nResearch Query: {query}\n\nSources:\n{context}\n\nProvide analysis with citations."
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response_post = requests.post(
                "https://api.cohere.ai/v1/generate",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                json={"model": "command", "prompt": prompt, "max_tokens": 4000, "temperature": 0.3, "stop_sequences": []},
                timeout=90  # increased timeout from 60 to 90 seconds
            )
            response_post.raise_for_status()
            result_json = response_post.json()
            return result_json["generations"][0]["text"]
        except requests.exceptions.Timeout as te:
            logger.warning("Cohere API timeout on attempt %d: %s", attempt, str(te))
            if attempt == max_retries:
                return f"Cohere API error: Read timed out after {max_retries} attempts. Please try again later."
            time.sleep(2)  # brief pause before retrying
        except Exception as e:
            logger.error("Cohere API error on attempt %d: %s", attempt, str(e))
            return f"Cohere API error: {str(e)}. Please verify your COHERE_API_KEY and your network connection."
    return "Cohere API error: Unable to obtain response."

def _generate_dummy_response(query: str, formatted_sources: List[Dict[str, Any]]) -> str:
    if not isinstance(query, str):
        logger.error("Invalid query.")
        return "Invalid query."
    try:
        keywords = [word for word in re.findall(r'\b\w+\b', query.lower()) if word not in {"a", "an", "the", "in", "on", "at", "for", "of"}]
        research_type = "market"
        if "competitor" in query.lower():
            research_type = "competitor"
        elif "trend" in query.lower():
            research_type = "trend"
        elif "customer" in query.lower():
            research_type = "customer"
        if research_type == "market":
            response = f"# Market Analysis: {', '.join(keywords[:3]).title()}\n\nSummary of market trends and potential."
        elif research_type == "competitor":
            response = f"# Competitor Analysis: {', '.join(keywords[:3]).title()}\n\nOverview of key competitors and SWOT."
        elif research_type == "trend":
            response = f"# Trend Analysis: {', '.join(keywords[:3]).title()}\n\nOverview of industry trends."
        else:
            response = "No dummy response available."
        return response
    except Exception as e:
        logger.error("Dummy response generation error: %s", str(e))
        return "Error generating dummy response."
        
if __name__ == "__main__":
    # Simple test to verify API integration functions
    sample_query = "Test market research"
    sample_results = [{"title": "Example", "url": "http://example.com", "content": "Example content", "accessed_date": "2023-10-10 12:00:00"}]
    print(generate_ai_response(sample_query, sample_results, model="Gemini"))
    print(generate_ai_response(sample_query, sample_results, model="Cohere"))
