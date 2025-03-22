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

# User-Agent list for randomization
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]


def get_website_text_content(url: str) -> str:
    """
    Extract the main text content from a website using trafilatura with fallback to BeautifulSoup.
    """
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=15)

        if not response.ok:
            logger.warning(
                f"Failed to retrieve content from {url}: HTTP Status {response.status_code}"
            )
            return ""

        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' not in content_type:
            logger.warning(
                f"Skipping non-HTML content from {url}: {content_type}")
            return ""

        content = trafilatura.extract(response.text)
        if content:
            return content

        # Fallback to BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ', strip=True)

        if not text or len(text.strip()) < 100:
            logger.warning(f"Insufficient text content extracted from {url}")
            return ""

        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error retrieving content from {url}: {str(e)}")
        return ""


def search_web(query: str,
               recency: str = "Past month",
               num_results: int = 10) -> List[Dict[str, str]]:
    """
    Search using SERP API.
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

    search = GoogleSearch({
        "q":
        query,
        "api_key":
        api_key,
        "num":
        num_results,
        "engine":
        "google",
        "tbs":
        f"qdr:{time_map.get(recency, 'm')}" if time_map.get(recency) else None,
        "safe":
        "active"
    })

    try:
        search_results = search.get_dict()
        return [{
            "title": result["title"],
            "url": result["link"],
            "snippet": result.get("snippet", "")
        } for result in search_results.get("organic_results", [])]
    except Exception as e:
        logger.error(f"Error searching Google: {str(e)}")
        return []


def search_and_extract_content(
        query: str,
        recency: str = "Past month",
        search_depth: int = 3,
        custom_urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Search for content and extract text from webpages.
    """
    search_categories = [{
        "name": "general",
        "query": query
    }, {
        "name": "business_viability",
        "query": f"{query} business viability"
    }, {
        "name": "competitors",
        "query": f"{query} competitors SWOT analysis"
    }, {
        "name": "audience",
        "query": f"{query} target audience demographics"
    }, {
        "name": "trends",
        "query": f"{query} industry trends"
    }, {
        "name": "regulatory",
        "query": f"{query} regulatory compliance"
    }]

    total_depth = search_depth
    results_per_category = max(1, total_depth // len(search_categories))
    all_search_results = search_web(query, recency, results_per_category * 2)

    if search_depth >= 3:
        for category in search_categories[1:]:
            category_results = search_web(category["query"], recency,
                                          results_per_category)
            for result in category_results:
                result["category"] = category["name"]
            all_search_results.extend(category_results)

    seen_urls = set()
    unique_results = []
    for result in all_search_results:
        if result["url"] not in seen_urls:
            seen_urls.add(result["url"])
            unique_results.append(result)

    if custom_urls:
        for url in custom_urls:
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.insert(
                    0, {
                        "title": f"Custom Source: {urlparse(url).netloc}",
                        "url": url,
                        "snippet": "User-provided source",
                        "category": "custom"
                    })

    results_with_content = []
    processed_count = 0
    random.shuffle(unique_results)

    for result in unique_results:
        if processed_count >= total_depth:
            break

        url = result["url"]
        parsed_url = urlparse(url)
        if any(
                parsed_url.netloc.endswith(ext) for ext in
            ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']):
            continue

        time.sleep(
            random.uniform(MIN_REQUEST_INTERVAL, MIN_REQUEST_INTERVAL * 2))

        try:
            logger.info(f"Extracting content from {url}")
            content = get_website_text_content(url)
            if not content or len(content.strip()) < 100:
                logger.warning(
                    f"Insufficient content extracted from {url}, skipping")
                continue

            max_content_length = 10000
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."

            result_with_content = {
                "title": result["title"],
                "url": url,
                "snippet": result["snippet"],
                "content": content,
                "accessed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": result.get("category", "general")
            }

            results_with_content.append(result_with_content)
            processed_count += 1
            logger.info(f"Processed {processed_count}/{total_depth}: {url}")
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")

    return results_with_content
