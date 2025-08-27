import yaml
from pathlib import Path
from typing import Dict, Any

class LangGraphAgent:
    def __init__(self, config_path: str):
        self.config = yaml.safe_load(Path(config_path).read_text())
        self.state: Dict[str, Any] = {}
        print(f"⚙️ Loaded pipeline config from {config_path}")

    def run(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        self.state.update(input_payload)

        for stage in self.config["stages"]:
            print(f"\n→ Stage: {stage['name']} ({stage['mode']})")

            for ability in stage["abilities"]:
                print(f" • Calling ability `{ability['name']}` on {ability['server']} with state: {self.state}")
                # TODO: replace with real call (HTTP, function, LLM, etc.)
                self.state[f"{stage['name']}_{ability['name']}"] = "done"

        return self.state
