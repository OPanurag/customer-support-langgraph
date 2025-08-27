"""
MCP client integrated with Knowledge Base retriever.

Responsibilities:
- Route KB queries to the retriever (via Retriever class).
- Provide explicit error for unimplemented abilities.
"""

import logging
from typing import Any, Dict

from .retriever import Retriever

logger = logging.getLogger(__name__)

# Initialize KB retriever once
kb_retriever = Retriever()


class MCPClientError(RuntimeError):
    pass


def call_common(ability_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route to COMMON abilities.
    Implemented abilities:
      - "faq_query" / "knowledge_base_search": uses Retriever.search
    """
    try:
        if ability_name in ("faq_query", "knowledge_base_search"):
            user_query = state.get("user_query") or state.get("query") or ""
            if not user_query:
                logger.warning("call_common: faq_query invoked with empty user_query")
                return {"kb_results": []}
            logger.info("COMMON -> executing KB query (faq_query): %s", user_query)
            kb_results = kb_retriever.search(user_query)
            return {"kb_results": kb_results}

        # Explicitly raise error for unimplemented abilities
        logger.error("COMMON -> Unimplemented ability called: %s", ability_name)
        raise MCPClientError(f"COMMON ability '{ability_name}' is not implemented.")
    except Exception as e:
        logger.exception("Error in call_common for ability %s: %s", ability_name, e)
        raise


def call_atlas(ability_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route to ATLAS abilities. Currently supports KB queries as well.
    """
    try:
        if ability_name in ("faq_query", "knowledge_base_search"):
            user_query = state.get("user_query") or state.get("query") or ""
            if not user_query:
                logger.warning("call_atlas: faq_query invoked with empty user_query")
                return {"kb_results": []}
            logger.info("ATLAS -> executing KB query (faq_query): %s", user_query)
            kb_results = kb_retriever.search(user_query)
            return {"kb_results": kb_results}

        logger.error("ATLAS -> Unimplemented ability called: %s", ability_name)
        raise MCPClientError(f"ATLAS ability '{ability_name}' is not implemented.")
    except Exception as e:
        logger.exception("Error in call_atlas for ability %s: %s", ability_name, e)
        raise
