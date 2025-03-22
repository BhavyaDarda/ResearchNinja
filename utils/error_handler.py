import logging
import traceback
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """
    Utility class for handling and formatting errors in a consistent way
    throughout the Research Ninja platform.
    """
    
    # Error type constants
    API_ERROR = "api_error"
    SEARCH_ERROR = "search_error"
    CONTENT_ERROR = "content_error"
    ANALYSIS_ERROR = "analysis_error"
    SYSTEM_ERROR = "system_error"
    
    # Error messages by type
    ERROR_MESSAGES = {
        API_ERROR: {
            "title": "API Error",
            "message": "There was an error connecting to an external API.",
            "suggestion": "Please check your API keys in the settings panel."
        },
        SEARCH_ERROR: {
            "title": "Search Error",
            "message": "Unable to perform the search operation.",
            "suggestion": "Please verify your API keys and internet connection."
        },
        CONTENT_ERROR: {
            "title": "Content Extraction Error",
            "message": "Could not retrieve content from some websites.",
            "suggestion": "Try adding specific URLs you want to analyze in Advanced Settings."
        },
        ANALYSIS_ERROR: {
            "title": "Analysis Error",
            "message": "Error occurred during content analysis.",
            "suggestion": "Try using a different AI model in the settings panel."
        },
        SYSTEM_ERROR: {
            "title": "System Error",
            "message": "An unexpected system error occurred.",
            "suggestion": "Please try again later or report this issue."
        }
    }
    
    @classmethod
    def format_error(cls, error_type: str, details: Optional[str] = None, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Format an error for consistent display to the user
        
        Args:
            error_type: Type of error (use class constants)
            details: Additional details about the error
            error: The exception object
            
        Returns:
            Formatted error dictionary
        """
        error_info = cls.ERROR_MESSAGES.get(error_type, cls.ERROR_MESSAGES[cls.SYSTEM_ERROR])
        
        # Create the base error response
        error_response = {
            "type": error_type,
            "title": error_info["title"],
            "message": error_info["message"],
            "suggestion": error_info["suggestion"],
            "details": details or ""
        }
        
        # Add technical details if an exception was provided
        if error:
            error_response["error_class"] = error.__class__.__name__
            error_response["error_message"] = str(error)
            
            # Log the full stack trace for debugging
            logger.error(f"Error ({error_type}): {str(error)}")
            logger.debug(traceback.format_exc())
            
        return error_response
    
    @classmethod
    def api_error(cls, api_name: str, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Format an API-related error
        
        Args:
            api_name: Name of the API that caused the error
            error: The exception object
            
        Returns:
            Formatted error dictionary
        """
        details = f"Error connecting to {api_name} API. Please verify your API key."
        return cls.format_error(cls.API_ERROR, details, error)
    
    @classmethod
    def search_error(cls, query: str, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Format a search-related error
        
        Args:
            query: The search query that caused the error
            error: The exception object
            
        Returns:
            Formatted error dictionary
        """
        details = f"Error searching for '{query}'. Please check your Bing API key."
        return cls.format_error(cls.SEARCH_ERROR, details, error)
    
    @classmethod
    def content_error(cls, url: str, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Format a content extraction error
        
        Args:
            url: The URL that caused the error
            error: The exception object
            
        Returns:
            Formatted error dictionary
        """
        details = f"Could not extract content from {url}."
        return cls.format_error(cls.CONTENT_ERROR, details, error)
    
    @classmethod
    def analysis_error(cls, model: str, error: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Format an analysis-related error
        
        Args:
            model: The AI model that caused the error
            error: The exception object
            
        Returns:
            Formatted error dictionary
        """
        details = f"Error during analysis with {model}. Please check your API key."
        return cls.format_error(cls.ANALYSIS_ERROR, details, error)