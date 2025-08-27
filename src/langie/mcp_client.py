"""
MCP client integrated with Knowledge Base retriever.
Routes abilities to KB (via retriever) instead of simulated responses.
"""

import logging
from typing import Any, Dict

# Import retriever functions
from .retriever import query_kb, index_kb

logger = logging.getLogger(__name__)

# Index KB on startup
try:
    index_kb()
    logger.info("Knowledge base indexed successfully on MCP startup.")
except Exception as e:
    logger.exception("Failed to index KB at startup: %s", e)


def call_common(ability_name: str, state: Dict[str, Any]) -> Any:
    """
    Route to COMMON abilities.
    For now: 
      - "faq_query" ability -> KB retrieval
      - others -> fallback to simulated response
    """
    try:
        if ability_name == "faq_query":
            user_query = state.get("user_query", "")
            if not user_query:
                return {"error": "No user_query provided"}
            
            logger.info("COMMON -> executing KB query: %s", user_query)
            return {"kb_results": query_kb(user_query)}

    except Exception as e:
        logger.exception("Error calling COMMON ability %s: %s", ability_name, e)

    # fallback simulation
    logger.info("COMMON -> simulated call for %s", ability_name)
    return {f"{ability_name}_status": "simulated_common_done"}


def call_atlas(ability_name: str, state: Dict[str, Any]) -> Any:
    """
    Route to ATLAS abilities.
    Currently identical to COMMON but allows extension later.
    """
    try:
        if ability_name == "faq_query":
            user_query = state.get("user_query", "")
            if not user_query:
                return {"error": "No user_query provided"}
            
            logger.info("ATLAS -> executing KB query: %s", user_query)
            return {"kb_results": query_kb(user_query)}

    except Exception as e:
        logger.exception("Error calling ATLAS ability %s: %s", ability_name, e)

    # fallback simulation
    logger.info("ATLAS -> simulated call for %s", ability_name)
    return {f"{ability_name}_status": "simulated_atlas_done"}
