import json
from pathlib import Path
from src.langie.pipeline import LangGraphAgent

def test_pipeline_smoke(sample_path="sample.json", config_path="config/stages.yaml"):
    """
    Run a full end-to-end smoke test of the LangGraphAgent pipeline.
    Reads sample JSON input, executes all stages, and prints debug info.
    """
    # Load sample input
    if not Path(sample_path).exists():
        raise FileNotFoundError(f"Sample file not found: {sample_path}")
    sample = json.loads(Path(sample_path).read_text())

    # Initialize pipeline agent
    agent = LangGraphAgent(config_path=config_path)

    # Run pipeline
    output = agent.run(sample)

    # --- DEBUG OUTPUT ---
    print("\n===== PIPELINE DEBUG OUTPUT =====")
    for k, v in output.items():
        if k != "logs":
            print(f"{k}: {v}")
    print("===== LOG EVENTS =====")
    for log in output.get("logs", []):
        print(f"{log['event']}: {log['payload']}")
    print("===========================\n")

    # --- ASSERTIONS ---
    assert output.get("ticket_id") == sample.get("ticket_id"), "Ticket ID mismatch"
    assert "logs" in output, "Logs not recorded"
    assert any(k in output for k in ["response", "ticket_status"]), "Response or ticket_status missing"
    assert "entities" in output, "Entities not extracted"
    assert "solution_score" in output, "Solution score missing"

    # Check KB retrieval
    kb_results = output.get("kb_results", [])
    assert isinstance(kb_results, list) and len(kb_results) > 0, "KB retrieval failed"

    print("✅ Pipeline smoke test passed.\n")
    return output


if __name__ == "__main__":
    result = test_pipeline_smoke()
