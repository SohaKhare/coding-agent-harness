from .agent import Agent
from .providers import GeminiProvider
from .tools import create_tool_registry


def main():

    print("Coding Agent")
    print("Type 'exit' to quit.\n")

    registry = create_tool_registry()
    provider = GeminiProvider()

    agent = Agent(
        tool_registry=registry,
        provider=provider,
        max_iterations=20,
    )

    while True:

        try:
            task = input(">>> ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not task:
            continue

        if task.lower() == "exit":
            break

        result = agent.run(task)

        print("\nFINAL:")
        print(result.final_response)

        print("\nTRACE:")

        for step in result.steps:
            print(
                f"Iteration {step.iteration}: "
                f"{step.tool_name}"
            )

        print()


if __name__ == "__main__":
    main()