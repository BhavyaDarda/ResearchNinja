import os
import json
import time
import logging
import random
import string
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_research_id() -> str:
    """
    Generate a unique ID for research sessions
    """
    timestamp = int(time.time())
    random_string = ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"research_{timestamp}_{random_string}"


def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """
    Extract key keywords from a text
    """
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = {
        'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was',
        'were', 'and', 'or', 'but', 'of'
    }
    filtered_words = [
        word for word in words if word not in stop_words and len(word) > 2
    ]
    word_counts = {
        word: filtered_words.count(word)
        for word in set(filtered_words)
    }
    sorted_words = sorted(word_counts.items(),
                          key=lambda x: x[1],
                          reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def parse_markdown_headings(markdown_text: str) -> Dict[str, str]:
    """
    Parse markdown text to extract sections based on headings
    """
    sections = {}
    current_section = "Main"
    current_content = []

    for line in markdown_text.split('\n'):
        if line.startswith('# '):
            sections[current_section] = '\n'.join(current_content)
            current_section = line[2:].strip()
            current_content = []
        else:
            current_content.append(line)

    sections[current_section] = '\n'.join(current_content)
    return sections


def format_timestamp(timestamp: Optional[str] = None,
                     format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a timestamp string or generate the current timestamp
    """
    try:
        dt = datetime.strptime(timestamp,
                               format_str) if timestamp else datetime.now()
    except ValueError:
        dt = datetime.now()
    return dt.strftime(format_str)


def cache_research_results(research_id: str,
                           data: Dict[str, Any],
                           expire_seconds: int = 3600) -> bool:
    """
    Cache research results to avoid redundant processing
    """
    try:
        cache_dir = os.path.join(os.path.dirname(__file__), '../.cache')
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, f"{research_id}.json")
        data['_cache_expires'] = (
            datetime.now() + timedelta(seconds=expire_seconds)).timestamp()
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        logger.error(f"Error caching research results: {e}")
        return False


def get_cached_research(research_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve cached research results if available and not expired
    """
    try:
        cache_dir = os.path.join(os.path.dirname(__file__), '../.cache')
        cache_file = os.path.join(cache_dir, f"{research_id}.json")
        if not os.path.exists(cache_file):
            return None
        with open(cache_file, 'r') as f:
            data = json.load(f)
        if '_cache_expires' in data and datetime.now().timestamp(
        ) > data['_cache_expires']:
            os.remove(cache_file)
            return None
        data.pop('_cache_expires', None)
        return data
    except Exception as e:
        logger.error(f"Error retrieving cached research: {e}")
        return None


def hash_query(query: str) -> str:
    """
    Create a hash of a query string for cache lookups
    """
    normalized_query = ' '.join(query.lower().split())
    return hashlib.md5(normalized_query.encode('utf-8')).hexdigest()
