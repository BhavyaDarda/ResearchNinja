import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ResearchNinjaClientError(Exception):
    """Custom exception for errors occurring in ResearchNinjaClient operations."""
    pass

class ResearchNinjaClient:
    """Helper class for integrating with the Research Ninja API."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        # Ensure the base_url does not end with a trailing slash.
        self.base_url = base_url.rstrip('/')
        logger.info(f"ResearchNinjaClient initialized with base URL: {self.base_url}")
        
    def create_research(self, query: str, model: str = "GPT-4o mini") -> Dict[str, Any]:
        """Create new research by calling the /research API endpoint."""
        try:
            logger.info(f"Creating research for query: {query} using model: {model}")
            response = requests.post(
                f"{self.base_url}/research",
                json={"query": query, "ai_model": model}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = f"Failed to create research: {str(e)}"
            logger.error(error_message)
            raise ResearchNinjaClientError(error_message) from e
    
    def get_research(self, research_id: str) -> Dict[str, Any]:
        """Retrieve research results by calling the /research/{research_id} endpoint."""
        try:
            logger.info(f"Retrieving research with ID: {research_id}")
            response = requests.get(f"{self.base_url}/research/{research_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = f"Failed to retrieve research with ID {research_id}: {str(e)}"
            logger.error(error_message)
            raise ResearchNinjaClientError(error_message) from e
    
    def export_research(self, research_id: str, format: str) -> Dict[str, Any]:
        """
        Export research in the specified format by calling the /export endpoint.
        The API expects the format string (e.g., 'PDF', 'JSON', etc.) in a case-insensitive manner.
        """
        try:
            logger.info(f"Exporting research {research_id} in format: {format}")
            response = requests.post(
                f"{self.base_url}/export",
                json={"research_id": research_id, "format": format}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = f"Failed to export research {research_id} in format {format}: {str(e)}"
            logger.error(error_message)
            raise ResearchNinjaClientError(error_message) from e
    
    def batch_export(self, research_id: str, formats: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Export research in multiple formats by calling the /batch-export endpoint.
        If a list of formats is supplied, they are joined as a comma-separated string.
        """
        try:
            formats_str = ",".join(formats) if formats else ""
            logger.info(f"Batch exporting research {research_id} in formats: {formats_str if formats_str else 'All'}")
            response = requests.get(
                f"{self.base_url}/batch-export/{research_id}",
                params={"formats": formats_str} if formats_str else None
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = f"Failed batch export for research {research_id}: {str(e)}"
            logger.error(error_message)
            raise ResearchNinjaClientError(error_message) from e
    
    def get_supported_formats(self) -> List[str]:
        """Retrieve a list of supported export formats by calling the /formats endpoint."""
        try:
            logger.info("Getting supported export formats.")
            response = requests.get(f"{self.base_url}/formats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_message = f"Failed to retrieve supported formats: {str(e)}"
            logger.error(error_message)
            raise ResearchNinjaClientError(error_message) from e