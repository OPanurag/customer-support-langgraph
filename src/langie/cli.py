import argparse

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
    print("🚀 Langie bot started... (placeholder)")


def test(args):
    print("✅ Running in test mode... everything looks good!")
