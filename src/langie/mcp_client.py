"""
MCP client integrated with Knowledge Base retriever.

Responsibilities:
- Route KB queries to the retriever (query_kb / index_kb).
- Provide a clear error for unimplemented abilities so integration is explicit.
- No silent dummy behavior: unhandled abilities raise an exception / return explicit error.
"""

import logging
from typing import Any, Dict

from .retriever import query_kb, index_kb

logger = logging.getLogger(__name__)

# Index KB on startup (idempotent)
try:
    index_kb()
    logger.info("Knowledge base indexed successfully on MCP startup.")
except Exception as e:
    logger.exception("Failed to index KB at startup: %s", e)


class MCPClientError(RuntimeError):
    pass


def call_common(ability_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route to COMMON abilities. Implemented abilities:
      - "faq_query" / "knowledge_base_search": uses retriever.query_kb
    Other abilities must be implemented explicitly to avoid silent fallbacks.
    """
    try:
        if ability_name in ("faq_query", "knowledge_base_search"):
            user_query = state.get("user_query") or state.get("query") or ""
            if not user_query:
                logger.warning("call_common: faq_query invoked with empty user_query")
                return {"kb_results": []}
            logger.info("COMMON -> executing KB query (faq_query): %s", user_query)
            kb = query_kb(user_query)
            return {"kb_results": kb}

        # Add explicit mappings for other COMMON abilities here if you implement them.
        logger.error("COMMON -> Unimplemented ability called: %s", ability_name)
        raise MCPClientError(f"COMMON ability '{ability_name}' is not implemented in mcp_client.")
    except Exception as e:
        logger.exception("Error in call_common for ability %s: %s", ability_name, e)
        raise


def call_atlas(ability_name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route to ATLAS abilities. Currently supports KB queries as well.
    Distinction left for future extension.
    """
    try:
        if ability_name in ("faq_query", "knowledge_base_search"):
            user_query = state.get("user_query") or state.get("query") or ""
            if not user_query:
                logger.warning("call_atlas: faq_query invoked with empty user_query")
                return {"kb_results": []}
            logger.info("ATLAS -> executing KB query (faq_query): %s", user_query)
            kb = query_kb(user_query)
            return {"kb_results": kb}

        logger.error("ATLAS -> Unimplemented ability called: %s", ability_name)
        raise MCPClientError(f"ATLAS ability '{ability_name}' is not implemented in mcp_client.")
    except Exception as e:
        logger.exception("Error in call_atlas for ability %s: %s", ability_name, e)
        raise
