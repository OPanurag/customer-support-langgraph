import yaml
from pathlib import Path
import logging
from typing import Dict, Any

from .mcp_client import call_common, call_atlas
from .models import InputPayload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class LangGraphAgent:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = yaml.safe_load(Path(config_path).read_text())
        self.state: Dict[str, Any] = {"logs": []}
        logger.info("⚙️ Loaded pipeline config from %s", config_path)

    def validate_input(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        validated = InputPayload.model_validate(payload)
        return validated.model_dump()

    def run(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        # validate & seed
        try:
            validated = self.validate_input(input_payload)
        except Exception as e:
            logger.error("Input validation failed: %s", e)
            raise
        self.state.update(validated)
        self._log("run_started", {"input_summary": {k: self.state.get(k) for k in ['ticket_id','customer_name']}})

        for stage in self.config.get("stages", []):
            name = stage["name"]
            mode = stage.get("mode", "deterministic")
            self._log("stage_start", {"stage": name, "mode": mode})

            if mode == "deterministic":
                for ability in stage.get("abilities", []):
                    self._execute_ability(name, ability)
            elif mode == "conditional":
                cond = stage.get("condition", "")
                if self._eval_condition(cond):
                    for ability in stage.get("abilities", []):
                        self._execute_ability(name, ability)
                else:
                    logger.info("Skipping conditional stage %s (cond=%s)", name, cond)
            elif mode == "non-deterministic":
                # execute solution_evaluation first, then possibly escalate
                # find solution_evaluation ability
                for ability in stage.get("abilities", []):
                    if ability["name"] == "solution_evaluation":
                        res = self._execute_ability(name, ability)
                        break
                score = self.state.get("solution_score", 0)
                if score < 90:
                    # escalate if configured
                    for ability in stage.get("abilities", []):
                        if ability["name"] == "escalation_decision":
                            self._execute_ability(name, ability)
                # always run update_payload if present
                for ability in stage.get("abilities", []):
                    if ability["name"] == "update_payload":
                        self._execute_ability(name, ability)
            else:
                logger.warning("Unknown stage mode %s for stage %s", mode, name)

            self._log("stage_end", {"stage": name})

        self._log("run_completed", {"final_keys": list(self.state.keys())})
        return self.state

    def _execute_ability(self, stage_name: str, ability: Dict[str, Any]) -> Any:
        name = ability["name"]
        server = ability.get("server", "COMMON")
        self._log("ability_start", {"stage": stage_name, "ability": name, "server": server})

        if server.upper() == "ATLAS":
            result = call_atlas(name, self.state)
        else:
            result = call_common(name, self.state)

        # merge dict results into state
        if isinstance(result, dict):
            self.state.update(result)
        else:
            self.state[f"{stage_name}_{name}"] = result or "done"

        self._log("ability_end", {"stage": stage_name, "ability": name, "result_summary": self._summarize(result)})
        return result

    def _eval_condition(self, cond: str) -> bool:
        # simple boolean expression interpreter for known tokens
        if not cond:
            return True
        cond = cond.lower()
        if "missing_entities" in cond and not self.state.get("entities"):
            return True
        if "low_confidence" in cond and self.state.get("solution_score", 100) < 80:
            return True
        # fallback: if any token 'or' present, evaluate loosely
        return False

    def _log(self, event: str, payload: Dict[str, Any]):
        logger.info("%s %s", event, payload)
        self.state.setdefault("logs", []).append({"event": event, "payload": payload})

    def _summarize(self, result: Any):
        if isinstance(result, dict):
            return {k: (v if isinstance(v,(int,str,bool)) else str(type(v))) for k,v in list(result.items())[:5]}
        return result
