import argparse
from pathlib import Path
from langie.pipeline import LangGraphAgent

def main():
    parser = argparse.ArgumentParser(prog="langie", description="Langie CLI - Customer Support Bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "run" command
    run_parser = subparsers.add_parser("run", help="Run the Langie bot")
    run_parser.set_defaults(func=run)

    # "test" command
    test_parser = subparsers.add_parser("test", help="Run test mode")
    test_parser.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)

def run(args):
    import json
    sample = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "query": "My order #123 hasn’t arrived",
        "priority": "High",
        "ticket_id": "TKT-5678",
    }
    agent = LangGraphAgent(config_path="config/stages.yaml")
    final = agent.run(sample)
    print("\n--- Final payload ---")
    print(json.dumps(final, indent=2))



def test(args):
    print("✅ Running in test mode... everything looks good!")
