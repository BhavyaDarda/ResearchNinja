import requests
from bs4 import BeautifulSoup
import trafilatura
import time
import random
from datetime import datetime
import os
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urlparse
from serpapi.google_search import GoogleSearch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting settings
MIN_REQUEST_INTERVAL = 1  # Minimum time between requests in seconds

# Maximum number of retries for retrieving content
MAX_RETRIES = 3

# User-Agent list for randomization (expanded with additional browser-like headers)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

def get_website_text_content(url: str) -> str:
    """
    Extract the main text content from a website using trafilatura.
    Retries the request up to MAX_RETRIES times on failure.
    Falls back to BeautifulSoup if trafilatura fails.

    Args:
         url: The website URL.

    Returns:
         Extracted text, or an empty string if extraction fails.
    """
    # Create a base headers template with conventional browser headers.
    base_headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": url
    }
    for attempt in range(1, MAX_RETRIES+1):
        try:
            response = requests.get(url, headers=base_headers, timeout=15)
            if not response.ok:
                logger.warning(f"[Attempt {attempt}] Failed to retrieve {url}: HTTP {response.status_code}")
                time.sleep(1)
                continue

            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                logger.warning(f"[Attempt {attempt}] Skipping non-HTML content from {url}: {content_type}")
                return ""

            # Attempt to extract text using trafilatura
            content = trafilatura.extract(response.text)
            if content and len(content.strip()) >= 100:
                return content

            # Fallback to BeautifulSoup if trafilatura extraction is insufficient
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=' ', strip=True)
            if text and len(text.strip()) >= 100:
                return text
            else:
                logger.warning(f"[Attempt {attempt}] Insufficient text content from {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"[Attempt {attempt}] Error retrieving {url}: {str(e)}")
        # Wait between retries
        time.sleep(1)
    # If all attempts fail, log and return an empty string
    logger.error(f"Failed to extract sufficient content from {url} after {MAX_RETRIES} attempts.")
    return ""

def search_web(query: str, recency: str = "Past month", num_results: int = 10) -> List[Dict[str, str]]:
    """
    Search for query results using the SERP API.

    Args:
         query: The search query.
         recency: Information recency filter.
         num_results: Number of results to return.

    Returns:
         A list of search result dicts with 'title', 'url', and optionally 'snippet'.
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        logger.warning("No SERP API key found.")
        return []

    time_map = {
        "Any time": None,
        "Past year": "y",
        "Past month": "m",
        "Past week": "w",
        "Past day": "d"
    }

    search_params = {
        "q": query,
        "api_key": api_key,
        "num": num_results,
        "engine": "google",
        "safe": "active"
    }
    # Set time-based filter if available
    tbs_value = time_map.get(recency)
    if tbs_value:
        search_params["tbs"] = f"qdr:{tbs_value}"

    try:
        search = GoogleSearch(search_params)
        search_results = search.get_dict()
        organic_results = search_results.get("organic_results", [])
        results = []
        for result in organic_results:
            results.append({
                "title": result.get("title", "No Title"),
                "url": result.get("link", ""),
                "snippet": result.get("snippet", "")
            })
        return results
    except Exception as e:
        logger.error(f"Error searching Google for query '{query}': {str(e)}")
        return []

def search_and_extract_content(query: str,
                               recency: str = "Past month",
                               search_depth: int = 3,
                               custom_urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Perform a search for content using the query, then extract text content from the URLs.
    This function categorizes search results and prioritizes user-provided custom URLs.

    Args:
         query: The research query.
         recency: Recency filter for search.
         search_depth: Number of pages/results to process.
         custom_urls: Optionally, list of user-provided URLs to include.

    Returns:
         A list of dictionaries with full content, metadata, and category.
    """
    search_categories = [
        {"name": "general", "query": query},
        {"name": "business_viability", "query": f"{query} business viability"},
        {"name": "competitors", "query": f"{query} competitors SWOT analysis"},
        {"name": "audience", "query": f"{query} target audience demographics"},
        {"name": "trends", "query": f"{query} industry trends"},
        {"name": "regulatory", "query": f"{query} regulatory compliance"}
    ]

    total_depth = search_depth
    results_per_category = max(1, total_depth // len(search_categories))
    all_search_results = search_web(query, recency, results_per_category * 2)

    # For additional category-specific searches (except 'general')
    if search_depth >= 3:
        for category in search_categories[1:]:
            category_results = search_web(category["query"], recency, results_per_category)
            for result in category_results:
                result["category"] = category["name"]
            all_search_results.extend(category_results)

    # Remove duplicate URLs
    seen_urls = set()
    unique_results = []
    for result in all_search_results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    # Prioritize user-supplied custom URLs
    if custom_urls:
        for url in custom_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.insert(0, {
                    "title": f"Custom Source: {urlparse(url).netloc}",
                    "url": url,
                    "snippet": "User-provided source",
                    "category": "custom"
                })

    results_with_content: List[Dict[str, Any]] = []
    processed_count = 0
    random.shuffle(unique_results)  # Randomize processing order
    for result in unique_results:
        if processed_count >= total_depth:
            break

        url = result.get("url", "")
        if not url:
            continue

        parsed_url = urlparse(url)
        if any(parsed_url.path.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']):
            logger.info(f"Skipping file URL: {url}")
            continue

        # Pause between requests to avoid rate limits.
        sleep_duration = random.uniform(MIN_REQUEST_INTERVAL, MIN_REQUEST_INTERVAL * 2)
        time.sleep(sleep_duration)

        try:
            logger.info(f"Extracting content from {url}")
            content = get_website_text_content(url)
            if not content or len(content.strip()) < 100:
                logger.warning(f"Insufficient content extracted from {url}, skipping")
                continue

            max_content_length = 10000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            result_with_content = {
                "title": result.get("title", "No Title"),
                "url": url,
                "snippet": result.get("snippet", ""),
                "content": content,
                "accessed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": result.get("category", "general")
            }
            results_with_content.append(result_with_content)
            processed_count += 1
            logger.info(f"Processed {processed_count}/{total_depth}: {url}")
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")

    if not results_with_content:
        logger.warning(f"No results with sufficient content were retrieved for query: {query}")
    return results_with_content