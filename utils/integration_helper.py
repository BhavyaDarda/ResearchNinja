
import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ResearchNinjaClient:
    """Helper class for integrating with Research Ninja API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        
    def create_research(self, query: str, model: str = "GPT-4o mini") -> Dict[str, Any]:
        """Create new research"""
        try:
            response = requests.post(
                f"{self.base_url}/research",
                json={"query": query, "ai_model": model}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Research creation failed: {str(e)}")
            raise
    
    def get_research(self, research_id: str) -> Dict[str, Any]:
        """Get research by ID"""
        try:
            response = requests.get(f"{self.base_url}/research/{research_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Research retrieval failed: {str(e)}")
            raise
    
    def export_research(self, research_id: str, format: str) -> Dict[str, Any]:
        """Export research in specified format"""
        try:
            response = requests.post(
                f"{self.base_url}/export",
                json={"research_id": research_id, "format": format}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            raise
    
    def batch_export(self, research_id: str, formats: Optional[List[str]] = None) -> Dict[str, Any]:
        """Export research in multiple formats"""
        try:
            formats_str = ",".join(formats) if formats else ""
            response = requests.get(
                f"{self.base_url}/batch-export/{research_id}",
                params={"formats": formats_str} if formats_str else None
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch export failed: {str(e)}")
            raise
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats"""
        try:
            response = requests.get(f"{self.base_url}/formats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get formats: {str(e)}")
            raise
