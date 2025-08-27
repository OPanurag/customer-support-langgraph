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

    # 🔎 Debug print before assertions
    print("\nDEBUG OUTPUT:", out, "\n")

    # ✅ Assertions (safety checks)
    assert out.get("ticket_id") == "TKT-5678"
    assert "logs" in out
    # Looser condition for now until we know the structure
    assert any(k in out for k in ["response", "ticket_status"])

    return out


if __name__ == "__main__":
    result = test_pipeline_smoke()
    print("\n===== PIPELINE OUTPUT =====")
    for k, v in result.items():
        print(f"{k}: {v}")
    print("===========================\n")
