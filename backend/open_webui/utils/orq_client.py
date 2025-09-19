"""
ORQ Client for Open WebUI Integration
"""

import logging
import json
import time
from typing import Optional, Dict, List, Any

from open_webui.config import ORQ_API_KEY
from open_webui.env import SRC_LOG_LEVELS
from orq_ai_sdk import Orq

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS.get("ORQ", logging.INFO))

class ORQClient:
    """ORQ Client for model discovery and chat completions"""
    
    def __init__(self):
        self.api_key = ORQ_API_KEY.value if ORQ_API_KEY.value else None
        
        # TODO: Replace with actual ORQ client initialization
        # Example:
        # from orq import Client
        # self.client = Client(api_key=self.api_key)
        self.client = Orq(
          api_key=self.api_key,
          environment="production",
        )
        
        log.info(f"ORQ Client initialized - API Key: {'✅ Set' if self.api_key else '❌ Missing'}")
    
    async def get_models(self) -> Dict[str, Any]:
        """
        Fetch available models from ORQ deployment
        
        Returns:
            dict: Raw ORQ models response
        """
        try:
            log.info("Fetching models from ORQ...")
            
            model = self.client.deployments.get_config(key="model", context={ "environments": ["production"]}).model
            
            return [
              {
                "id": model,
                "name": model,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "orq",
                "orq": model,
                "connection_type": "orq",
                "tags": [],
              }
            ]
            
        except Exception as e:
            log.error(f"Failed to fetch ORQ models: {e}")
            raise e

# Global ORQ client instance
_orq_client: Optional[ORQClient] = None

def get_orq_client() -> Optional[ORQClient]:
    """Get or create the global ORQ client instance"""
    global _orq_client
    if _orq_client is None:
        _orq_client = ORQClient()
    return _orq_client
