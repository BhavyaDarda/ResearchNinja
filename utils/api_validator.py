import os
import re
import logging
from typing import Dict, List, Optional, Any

# Configure logging for the module.
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class APIKeyValidator:
    """
    Handles API key validation and storage for Research Ninja.
    
    API_CONFIG contains configurations for the supported APIs.
    SECURE_STORAGE is used for temporary (in-memory) storage of keys.
    """
    
    API_CONFIG: Dict[str, Dict[str, Any]] = {
        "SERP_API_KEY": {
            "name": "SERP API",
            "required": True,
            "description": "Used for real-time web search. Essential for research.",
            "url": "https://serpapi.com/dashboard"
        },
        "GEMINI_API_KEY": {
            "name": "Google Gemini API",
            "required": False,
            "description": "Used when selecting the Gemini model for analysis.",
            "url": "https://ai.google.dev/tutorials/setup"
        },
        "COHERE_API_KEY": {
            "name": "Cohere API",
            "required": False,
            "description": "Used for inquiries with the Cohere model.",
            "url": "https://dashboard.cohere.ai/api-keys"
        }
    }
    
    # In-memory storage of API keys; in production, secure persistent storage is recommended.
    SECURE_STORAGE: Dict[str, str] = {}

    @classmethod
    def get_missing_api_keys(cls, selected_model: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Returns a list of dictionaries for API keys that are missing based on the selected model.
        The SERP API key is always required.
        """
        missing_keys: List[Dict[str, str]] = []
        
        if not cls.get_api_key("SERP_API_KEY"):
            missing_keys.append({
                "key": "SERP_API_KEY",
                "name": cls.API_CONFIG["SERP_API_KEY"]["name"],
                "description": cls.API_CONFIG["SERP_API_KEY"]["description"],
                "url": cls.API_CONFIG["SERP_API_KEY"]["url"]
            })
        
        if selected_model:
            if selected_model == "Gemini" and not cls.get_api_key("GEMINI_API_KEY"):
                missing_keys.append({
                    "key": "GEMINI_API_KEY",
                    "name": cls.API_CONFIG["GEMINI_API_KEY"]["name"],
                    "description": cls.API_CONFIG["GEMINI_API_KEY"]["description"],
                    "url": cls.API_CONFIG["GEMINI_API_KEY"]["url"]
                })
            elif selected_model == "Claude" and not cls.get_api_key("ANTHROPIC_API_KEY"):
                missing_keys.append({
                    "key": "ANTHROPIC_API_KEY",
                    "name": cls.API_CONFIG["ANTHROPIC_API_KEY"]["name"],
                    "description": cls.API_CONFIG["ANTHROPIC_API_KEY"]["description"],
                    "url": cls.API_CONFIG["ANTHROPIC_API_KEY"]["url"]
                })
            elif selected_model == "Cohere" and not cls.get_api_key("COHERE_API_KEY"):
                missing_keys.append({
                    "key": "COHERE_API_KEY",
                    "name": cls.API_CONFIG["COHERE_API_KEY"]["name"],
                    "description": cls.API_CONFIG["COHERE_API_KEY"]["description"],
                    "url": cls.API_CONFIG["COHERE_API_KEY"]["url"]
                })

        return missing_keys

    @classmethod
    def get_api_key(cls, key_name: str) -> Optional[str]:
        """
        Retrieve the API key from SECURE_STORAGE first, then fall back to environment variables.
        """
        stored_key = cls.SECURE_STORAGE.get(key_name)
        if stored_key:
            return stored_key
        return os.getenv(key_name)

    @classmethod
    def save_api_key(cls, key_name: str, value: str) -> bool:
        """
        Validate and save the API key into secure storage and environment variables.
        Returns True if the key is valid and saved, otherwise False.
        """
        try:
            if key_name in cls.API_CONFIG and value and value.strip():
                cleaned_key = value.strip()
                if not cls.validate_api_key(key_name, cleaned_key):
                    logger.warning(f"Invalid format for API key: {key_name}.")
                    return False
                if not cls.test_api_key(key_name, cleaned_key):
                    logger.warning(f"Failed to verify API key for: {key_name}.")
                    return False
                
                cls.SECURE_STORAGE[key_name] = cleaned_key
                os.environ[key_name] = cleaned_key  # For backward compatibility.
                logger.info(f"API key for {key_name} has been saved and validated.")
                return True
            else:
                logger.warning(f"API key parameters invalid for: {key_name}.")
                return False
        except Exception as e:
            logger.error(f"Error saving API key {key_name}: {str(e)}")
            return False

    @classmethod
    def test_api_key(cls, key_name: str, value: str) -> bool:
        """
        Test the API key by making a minimal API request.
        Returns True if the key appears valid; otherwise, returns False.
        Enhanced error handling provides more detail on failures.
        """
        try:
            if key_name == "OPENAI_API_KEY":
                import openai
                openai.api_key = value
                try:
                    openai.Model.list()
                    return True
                except Exception as inner_e:
                    logger.error(f"OpenAI API test failed for {key_name}: {str(inner_e)}")
                    return False
            elif key_name == "SERP_API_KEY":
                from serpapi.google_search import GoogleSearch
                search = GoogleSearch({"q": "test", "api_key": value, "num": 1})
                res = search.get_dict()
                return "organic_results" in res
            elif key_name == "GEMINI_API_KEY":
                import requests
                url = f"https://generativelanguage.googleapis.com/v1/models?key={value}"
                response = requests.get(url, timeout=15)
                return response.status_code == 200
            elif key_name == "ANTHROPIC_API_KEY":
                import requests
                headers = {"x-api-key": value}
                response = requests.get("https://api.anthropic.com/v1/models", headers=headers, timeout=15)
                return response.status_code == 200
            elif key_name == "COHERE_API_KEY":
                import requests
                headers = {"Authorization": f"Bearer {value}"}
                response = requests.get("https://api.cohere.ai/v1/models", headers=headers, timeout=15)
                return response.status_code == 200
            # If no specific test exists, consider the key valid if non-empty.
            return True
        except Exception as e:
            logger.error(f"API key test failed for {key_name}: {str(e)}")
            return False

    @classmethod
    def validate_api_key(cls, key_name: str, value: str) -> bool:
        """
        Validate the API key format.
        Ensures the key is non-empty, of sufficient length, and meets provider-specific criteria.
        """
        if not value or len(value.strip()) < 10:
            logger.error(f"API key for {key_name} is too short or empty.")
            return False
        
        key = value.strip()
        if not re.match(r'^[A-Za-z0-9\-_]+$', key):
            logger.error(f"API key for {key_name} contains invalid characters.")
            return False

        if key_name == "SERP_API_KEY" and len(key) != 64:
            logger.error("SERP API key must be exactly 64 characters long.")
            return False
        if key_name == "GEMINI_API_KEY" and not re.match(r'^[A-Za-z0-9\-_]{39}$', key):
            logger.error("Gemini API key format is invalid.")
            return False
        if key_name == "COHERE_API_KEY" and not key.startswith("co-"):
            logger.error("Cohere API key must begin with 'co-'.")
            return False
        if re.search(r'[<>&;]', key):
            logger.error(f"API key for {key_name} contains forbidden characters.")
            return False
        
        return True

    @classmethod
    def get_api_key_info(cls, key_name: str) -> Dict[str, Any]:
        """
        Retrieve the configuration info of the specified API key.
        """
        return cls.API_CONFIG.get(key_name, {
            "name": key_name,
            "required": False,
            "description": "Unknown API key",
            "url": ""
        })

if __name__ == "__main__":
    # Quick test stub for manual execution.
    test_key = "sk-testexamplekey1234567890"
    if APIKeyValidator.validate_api_key("GEMINI_API_KEY", test_key):
        print("API Key validated.")
    else:
        print("API Key invalid.")