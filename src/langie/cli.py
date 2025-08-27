import argparse
from pathlib import Path
from langie.pipeline import LangGraphAgent

def main():
    parser = argparse.ArgumentParser(prog="langie", description="Langie CLI - Customer Support Bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the Langie bot")
    run_parser.add_argument("--config", "-c", default="config/stages.yaml",
                             help="Path to stages YAML")
    run_parser.add_argument("--input", "-i", default=None,
                             help="Path to JSON file with input payload (optional)")
    run_parser.set_defaults(func=run)

    test_parser = subparsers.add_parser("test", help="Run test mode")
    test_parser.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)


def run(args):
    import json
    from pathlib import Path

    sample = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "query": "My order #123 hasn’t arrived",
        "priority": "High",
        "ticket_id": "TKT-5678",
    }
    if args.input:
        sample = json.loads(Path(args.input).read_text())

    agent = LangGraphAgent(config_path=args.config)
    final = agent.run(sample)

    print("\n--- Final payload ---")
    print(json.dumps(final, indent=2))
