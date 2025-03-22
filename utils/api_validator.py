import os
import re
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIKeyValidator:
    """
    Utility class for validating and managing API keys for the Research Ninja platform.
    This ensures consistent API key handling throughout the application.
    """

    # Define required API models and their corresponding environment variables
    API_CONFIG = {
        "SERP_API_KEY": {
            "name": "SERP API",
            "required": True,
            "description": "Required for real-time web search. All research depends on this API.",
            "url": "https://serpapi.com/dashboard"
        },
        "OPENAI_API_KEY": {
            "name": "OpenAI API",
            "required": False,
            "description": "Required when using GPT-4o mini model for analysis.",
            "url": "https://platform.openai.com/api-keys"
        },
        "GEMINI_API_KEY": {
            "name": "Google Gemini API",
            "required": False,
            "description": "Required when using Gemini model for analysis.",
            "url": "https://ai.google.dev/tutorials/setup"
        },
        "ANTHROPIC_API_KEY": {
            "name": "Anthropic API",
            "required": False,
            "description": "Required when using Claude model for analysis.",
            "url": "https://console.anthropic.com/keys"
        },
        "COHERE_API_KEY": {
            "name": "Cohere API",
            "required": False,
            "description": "Required when using Cohere model for analysis.",
            "url": "https://dashboard.cohere.ai/api-keys"
        }
    }

    @classmethod
    def get_missing_api_keys(cls, selected_model: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Check for missing API keys based on the selected model

        Args:
            selected_model: The AI model selected by the user

        Returns:
            A list of missing API key details
        """
        missing_keys = []

        # Check for SERP API (always required)
        if not os.getenv("SERP_API_KEY"):
            missing_keys.append({
                "key": "SERP_API_KEY",
                "name": cls.API_CONFIG["SERP_API_KEY"]["name"],
                "description": cls.API_CONFIG["SERP_API_KEY"]["description"],
                "url": cls.API_CONFIG["SERP_API_KEY"]["url"]
            })

        # Check for model-specific API keys
        if selected_model:
            if selected_model == "GPT-4o mini" and not os.getenv("OPENAI_API_KEY"):
                missing_keys.append({
                    "key": "OPENAI_API_KEY",
                    "name": cls.API_CONFIG["OPENAI_API_KEY"]["name"],
                    "description": cls.API_CONFIG["OPENAI_API_KEY"]["description"],
                    "url": cls.API_CONFIG["OPENAI_API_KEY"]["url"]
                })
            elif selected_model == "Gemini" and not os.getenv("GEMINI_API_KEY"):
                missing_keys.append({
                    "key": "GEMINI_API_KEY",
                    "name": cls.API_CONFIG["GEMINI_API_KEY"]["name"],
                    "description": cls.API_CONFIG["GEMINI_API_KEY"]["description"],
                    "url": cls.API_CONFIG["GEMINI_API_KEY"]["url"]
                })
            elif selected_model == "Claude" and not os.getenv("ANTHROPIC_API_KEY"):
                missing_keys.append({
                    "key": "ANTHROPIC_API_KEY",
                    "name": cls.API_CONFIG["ANTHROPIC_API_KEY"]["name"],
                    "description": cls.API_CONFIG["ANTHROPIC_API_KEY"]["description"],
                    "url": cls.API_CONFIG["ANTHROPIC_API_KEY"]["url"]
                })
            elif selected_model == "Cohere" and not os.getenv("COHERE_API_KEY"):
                missing_keys.append({
                    "key": "COHERE_API_KEY",
                    "name": cls.API_CONFIG["COHERE_API_KEY"]["name"],
                    "description": cls.API_CONFIG["COHERE_API_KEY"]["description"],
                    "url": cls.API_CONFIG["COHERE_API_KEY"]["url"]
                })

        return missing_keys

    @classmethod
    def save_api_key(cls, key_name: str, value: str) -> bool:
        """
        Save an API key to the environment and persist it

        Args:
            key_name: The name of the API key (e.g., "OPENAI_API_KEY")
            value: The API key value

        Returns:
            True if the key was saved successfully, False otherwise
        """
        try:
            if key_name in cls.API_CONFIG and value and len(value.strip()) > 0:
                # Save to environment
                os.environ[key_name] = value.strip()

                # Validate the key format
                if not cls.validate_api_key(key_name, value):
                    logger.warning(f"Invalid API key format for {key_name}")
                    return False

                # Test the key with a minimal API call
                if not cls.test_api_key(key_name, value):
                    logger.warning(f"API key validation failed for {key_name}")
                    return False

                logger.info(f"API key saved and validated: {key_name}")
                return True
            else:
                logger.warning(f"Invalid API key parameters: {key_name}")
                return False
        except Exception as e:
            logger.error(f"Error saving API key {key_name}: {str(e)}")
            return False

    @classmethod
    def test_api_key(cls, key_name: str, value: str) -> bool:
        """Test if the API key is valid by making a minimal API call"""
        try:
            if key_name == "OPENAI_API_KEY":
                import openai
                openai.api_key = value
                openai.Model.list()
                return True
            elif key_name == "SERP_API_KEY":
                from serpapi import GoogleSearch
                search = GoogleSearch({"q": "test", "api_key": value, "num": 1})
                search.get_dict()
                return True
            elif key_name == "GEMINI_API_KEY":
                import requests
                url = f"https://generativelanguage.googleapis.com/v1beta/models?key={value}"
                response = requests.get(url)
                return response.status_code == 200
            elif key_name == "ANTHROPIC_API_KEY":
                import requests
                headers = {"x-api-key": value}
                response = requests.get(
                    "https://api.anthropic.com/v1/models",
                    headers=headers
                )
                return response.status_code == 200
            elif key_name == "COHERE_API_KEY":
                import requests
                headers = {"Authorization": f"Bearer {value}"}
                response = requests.get(
                    "https://api.cohere.ai/v1/models",
                    headers=headers
                )
                return response.status_code == 200
            return True
        except Exception as e:
            logger.error(f"API key test failed for {key_name}: {str(e)}")
            return False

    @classmethod
    def validate_api_key(cls, key_name: str, value: str) -> bool:
        """
        Validate an API key (basic format check)

        Args:
            key_name: The name of the API key
            value: The API key value

        Returns:
            True if the key format is valid, False otherwise
        """
        # Enhanced validation
        if not value:
            logger.error(f"Empty API key provided for {key_name}")
            return False
            
        value = value.strip()
        if len(value) < 10:
            logger.error(f"API key too short for {key_name}")
            return False
            
        if not re.match(r'^[A-Za-z0-9\-_]+$', value):
            logger.error(f"Invalid characters in API key for {key_name}")
            return False

        # Specific validations by provider
        if key_name == "OPENAI_API_KEY" and not value.startswith("sk-"):
            return False
        elif key_name == "ANTHROPIC_API_KEY" and not value.startswith(("sk-", "ant-")):
            return False
        elif key_name == "SERP_API_KEY" and len(value.strip()) != 64:
            return False
        elif key_name == "GEMINI_API_KEY" and not re.match(r'^[A-Za-z0-9-_]{39}$', value):
            return False
        elif key_name == "COHERE_API_KEY" and not value.startswith(("co-")):
            return False

        # Check for invalid characters
        if re.search(r'[<>&;]', value):
            return False

        return True

    @classmethod
    def get_api_key_info(cls, key_name: str) -> Dict[str, Any]:
        """
        Get information about an API key

        Args:
            key_name: The name of the API key

        Returns:
            A dictionary with API key information
        """
        if key_name in cls.API_CONFIG:
            return cls.API_CONFIG[key_name]
        else:
            return {
                "name": key_name,
                "required": False,
                "description": "Unknown API key",
                "url": ""
            }