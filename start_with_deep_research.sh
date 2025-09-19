#!/bin/bash

# Load deep research configuration
export ENABLE_DEEP_RESEARCH_MODE=true
export DEEP_RESEARCH_MODEL_PRIMARY=mistral:7b
export DEEP_RESEARCH_MODEL_SECONDARY=mistral:7b
export DEEP_RESEARCH_SYNTHESIS_MODEL=mistral:7b
export DEEP_RESEARCH_MAX_ITERATIONS=3
export DEEP_RESEARCH_RAG_TOP_K=10

# Load Perplexity configuration (you need to set your API key)
export ENABLE_WEB_SEARCH=true
export WEB_SEARCH_ENGINE=perplexity
export PERPLEXITY_API_KEY=your_perplexity_api_key_here
export PERPLEXITY_MODEL=sonar-deep-research
export PERPLEXITY_SEARCH_CONTEXT_USAGE=high
export WEB_SEARCH_RESULT_COUNT=5

echo "Starting Open WebUI with Deep Research enabled..."
echo "Make sure to set your PERPLEXITY_API_KEY in this script!"

# Start the server
cd backend
source ../.venv/bin/activate
python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --forwarded-allow-ips '*' --reload
