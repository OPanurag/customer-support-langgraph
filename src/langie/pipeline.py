import yaml
from typing import Dict, Any, Callable
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .abilities import call_common, call_atlas
from .retriever import query_kb
from .logger import logger


# -------- State Definition --------
class PipelineState(Dict[str, Any]):
    """Shared state passed between graph nodes."""
    pass


# -------- Ability Wrappers --------
def run_common(state: PipelineState, ability: str, params: Dict[str, Any]) -> PipelineState:
    logger.info(f"[COMMON] Running ability={ability} with params={params}")
    result = call_common(ability, params)
    state[ability] = result
    return state


def run_atlas(state: PipelineState, ability: str, params: Dict[str, Any]) -> PipelineState:
    logger.info(f"[ATLAS] Running ability={ability} with params={params}")
    result = call_atlas(ability, params)
    state[ability] = result
    return state


def run_retriever(state: PipelineState, query: str) -> PipelineState:
    logger.info(f"[RETRIEVER] Querying KB with: {query}")
    result = query_kb(query)
    state["retriever_result"] = result
    return state


# -------- Graph Orchestrator --------
class LangGraphAgent:
    def __init__(self, config_path: str = "config/stages.yaml"):
        self.config_path = config_path
        self.graph = None
        self.state = PipelineState()
        self._load_config_and_build()

    def _load_config_and_build(self):
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        stages = config.get("stages", [])
        logger.info(f"⚙️ Loaded {len(stages)} stages from {self.config_path}")

        # Create LangGraph
        workflow = StateGraph(PipelineState)

        # Dynamically add nodes
        for idx, stage in enumerate(stages):
            stage_name = stage["name"]
            ability = stage["ability"]
            ability_type = stage.get("type", "common")
            params = stage.get("params", {})

            def make_node(stage_name=stage_name, ability=ability,
                          ability_type=ability_type, params=params) -> Callable:
                def node_fn(state: PipelineState) -> PipelineState:
                    if ability_type == "common":
                        return run_common(state, ability, params)
                    elif ability_type == "atlas":
                        return run_atlas(state, ability, params)
                    elif ability_type == "retriever":
                        query = state.get("query", params.get("query", ""))
                        return run_retriever(state, query)
                    else:
                        raise ValueError(f"Unknown ability_type={ability_type}")
                return node_fn

            workflow.add_node(stage_name, make_node())

            # Link stages linearly (can extend later with conditional routing)
            if idx > 0:
                prev_stage = stages[idx - 1]["name"]
                workflow.add_edge(prev_stage, stage_name)

        # Last stage leads to END
        if stages:
            workflow.add_edge(stages[-1]["name"], END)

        # Compile graph with in-memory checkpointing
        memory = MemorySaver()
        self.graph = workflow.compile(checkpointer=memory)
        logger.info("✅ LangGraph pipeline built successfully")

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"▶️ Starting pipeline run with input={input_data}")
        self.state.update(input_data)
        final_state = self.graph.invoke(self.state)
        logger.info(f"🏁 Pipeline completed. Final state keys: {list(final_state.keys())}")
        return final_state
