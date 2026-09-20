import argparse
from pathlib import Path

from agent_learning.agent import Agent
from agent_learning.evaluator import Evaluator
from agent_learning.tools import create_tool_registry

from tests.eval_cases import CASES
from agent_learning.providers import GeminiProvider

def main():

    parser = argparse.ArgumentParser(
        description="Run coding-agent evaluations."
    )

    parser.add_argument(
        "--case",
        help="Run a specific evaluation case.",
    )

    args = parser.parse_args()

    workspace = (
        Path(__file__)
        .resolve()
        .parents[1]
        / "workspace"
    )

    registry = create_tool_registry()

    provider = GeminiProvider()

    agent = Agent(
        tool_registry=registry,
        provider=provider,
        max_iterations=10,
    )

    evaluator = Evaluator(
        agent=agent,
        workspace=workspace,
    )

    cases = CASES

    if args.case:
        cases = [
            case
            for case in CASES
            if case.name == args.case
        ]

        if not cases:
            print(
                f"Unknown evaluation case: "
                f"{args.case}"
            )

            print("\nAvailable cases:")

            for case in CASES:
                print(f"  {case.name}")

            return

    results = evaluator.run_all(cases)

    print("\n=== EVALUATION RESULTS ===\n")

    passed = 0

    for result in results:

        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        print(
            f"[{status}] {result.name}"
        )

        print(
            f"  Iterations: {result.iterations}"
        )

        print(
            f"  Tools: {result.tools_used}"
        )

        if result.error:
            print(
                f"  Error: {result.error}"
            )

        print()

        if result.passed:
            passed += 1

    print(
        f"Score: {passed}/{len(results)}"
    )


if __name__ == "__main__":
    main()