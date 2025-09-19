"""
ORQ Router for Open WebUI Integration
Handles chat completions and configuration for ORQ models
"""

import logging
import json
from typing import Optional, Dict, List, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from open_webui.models.users import UserModel
from open_webui.utils.auth import get_admin_user, get_verified_user
from open_webui.utils.orq_client import get_orq_client
from open_webui.config import ENABLE_ORQ_API, ORQ_API_KEY
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS.get("ORQ", logging.INFO))

router = APIRouter()

# Configuration Models
class ORQConfigForm(BaseModel):
    ENABLE_ORQ_API: Optional[bool] = None
    ORQ_API_KEY: str

@router.get("/config")
async def get_config(request: Request, user=Depends(get_admin_user)):
    """Get ORQ configuration"""
    return {
        "ENABLE_ORQ_API": request.app.state.config.ENABLE_ORQ_API,
        "ORQ_API_KEY": request.app.state.config.ORQ_API_KEY,
    }

@router.post("/config/update")
async def update_config(
    request: Request, form_data: ORQConfigForm, user=Depends(get_admin_user)
):
    """Update ORQ configuration"""
    request.app.state.config.ENABLE_ORQ_API = form_data.ENABLE_ORQ_API
    request.app.state.config.ORQ_API_KEY = form_data.ORQ_API_KEY
    
    # Reinitialize client with new settings
    from open_webui.utils.orq_client import _orq_client
    global _orq_client
    _orq_client = None  # Force recreation with new config
    
    return {
        "ENABLE_ORQ_API": request.app.state.config.ENABLE_ORQ_API,
        "ORQ_API_KEY": "***" if request.app.state.config.ORQ_API_KEY else "",
    }

# Chat Completion Models
class ORQMessage(BaseModel):
    role: str
    content: str

class ORQChatCompletionForm(BaseModel):
    model: str
    messages: List[ORQMessage]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None

@router.post("/chat/completions")
async def generate_chat_completion(
    request: Request,
    form_data: ORQChatCompletionForm,
    user=Depends(get_verified_user),
):
    """
    Generate chat completion using ORQ
    """
    try:
        orq_client = get_orq_client()
        if not orq_client:
            raise HTTPException(status_code=503, detail="ORQ client not available")
        
        if not orq_client.api_key:
            raise HTTPException(status_code=401, detail="ORQ API key not configured")
        
        log.info(f"ORQ chat completion request for model: {form_data.model}")
        
        # TODO: Implement actual ORQ chat completion call
        # This is where you'll call the ORQ SDK for chat completions
        # Example:
        # response = await orq_client.client.chat.completions.create(
        #     model=form_data.model,
        #     messages=[msg.dict() for msg in form_data.messages],
        #     stream=form_data.stream,
        #     temperature=form_data.temperature,
        #     max_tokens=form_data.max_tokens
        # )
        
        # For now, return a mock response in OpenAI format
        mock_response = {
            "id": "chatcmpl-orq-test",
            "object": "chat.completion",
            "created": 1234567890,
            "model": form_data.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"Mock response from ORQ model {form_data.model}. User said: {form_data.messages[-1].content}"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        
        log.info("ORQ chat completion successful")
        return mock_response
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"ORQ chat completion failed: {e}")
        raise HTTPException(status_code=500, detail=f"ORQ completion failed: {str(e)}")

@router.get("/models")
async def get_models(request: Request, user=Depends(get_verified_user)):
    """
    Get available ORQ models
    """
    try:
        orq_client = get_orq_client()
        if not orq_client:
            return {"data": []}
        
        models = await orq_client.get_models()
        return {"data": models}
        
    except Exception as e:
        log.error(f"Failed to fetch ORQ models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

@router.post("/verify")
async def verify_connection(request: Request, user=Depends(get_admin_user)):
    """
    Verify ORQ connection
    """
    try:
        orq_client = get_orq_client()
        if not orq_client:
            return {"status": "error", "message": "ORQ client not initialized"}
        
        if not orq_client.api_key:
            return {"status": "error", "message": "ORQ API key not configured"}
        
        # Test connection by fetching models
        models = await orq_client.get_models()
        
        return {
            "status": "success",
            "message": f"ORQ connection successful. Found {len(models)} models.",
            "models_count": len(models)
        }
        
    except Exception as e:
        log.error(f"ORQ connection verification failed: {e}")
        return {"status": "error", "message": str(e)}
