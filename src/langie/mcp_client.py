# src/langie/mcp_client.py
"""
Simple MCP client router for demo. It either calls local ability implementations
(if present) or simulates an external call and returns a canned response.
"""
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

def call_common(ability_name: str, state: Dict[str, Any]) -> Any:
    # Local dispatch if ability exists in abilities module
    try:
        from . import abilities
        fn = getattr(abilities, ability_name, None)
        if callable(fn):
            logger.info("COMMON -> executing local ability %s", ability_name)
            return fn(state)
    except Exception as e:
        logger.exception("Error calling local COMMON ability: %s", e)
    # fallback simulation
    logger.info("COMMON -> simulated call for %s", ability_name)
    return {f"{ability_name}_status": "simulated_common_done"}

def call_atlas(ability_name: str, state: Dict[str, Any]) -> Any:
    try:
        from . import abilities
        fn = getattr(abilities, ability_name, None)
        if callable(fn):
            logger.info("ATLAS -> executing local ability %s", ability_name)
            # abilities may accept server flag
            try:
                return fn(state, server="ATLAS")
            except TypeError:
                return fn(state)
    except Exception as e:
        logger.exception("Error calling local ATLAS ability: %s", e)
    logger.info("ATLAS -> simulated remote call for %s", ability_name)
    return {f"{ability_name}_status": "simulated_atlas_done"}
