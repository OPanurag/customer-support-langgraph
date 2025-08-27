from src.langie.pipeline import LangGraphAgent

def test_pipeline_smoke():
    cfg = "config/stages.yaml"
    agent = LangGraphAgent(config_path=cfg)
    sample = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "query": "My order #123 hasn’t arrived",
        "priority": "High",
        "ticket_id": "TKT-5678",
    }
    out = agent.run(sample)
    assert out.get("ticket_id") == "TKT-5678"
    assert "logs" in out
    assert "response" in out or out.get("ticket_status") is not None
