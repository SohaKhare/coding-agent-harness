from dataclasses import dataclass, field
from typing import Any

from google.genai import types

from .context import ContextManager
from .provider import LLMProvider
from .registry import ToolRegistry

SYSTEM_INSTRUCTION = """
You are a coding agent operating inside a workspace.

Your job is to modify and work with the user's codebase using
the available tools.

Rules:

1. Inspect the workspace before making significant changes.
2. Read relevant files before editing them.
3. Prefer edit_file for modifying existing files.
4. Use write_file for creating new files.
5. Use search_files when you need to find code or references.
6. When the user asks you to run or test code, actually use
   run_command.
7. Reading a file does not count as execution.
8. Pay attention to tool errors and recover from them.
9. If a tool fails because of an incorrect argument, fix the
   argument and try again when possible.
10. If a file does not exist, inspect the workspace or search
    for the correct path before retrying.
11. If a command fails, inspect the error and determine whether
    the code or command should be corrected.
12. Do not blindly repeat the exact same failed tool call.
13. After making code changes, run appropriate tests or commands
    when possible.
14. Do not claim that code works unless you have actually
    verified it.
15. Keep changes focused on the user's request.
"""


@dataclass
class AgentStep:
    iteration: int
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    result: Any = None


@dataclass
class AgentResult:
    final_response: str
    steps: list[AgentStep] = field(
        default_factory=list
    )


class Agent:

    def __init__(
        self,
        tool_registry: ToolRegistry,
        provider: LLMProvider,
        max_iterations: int = 20,
    ):
        self.tool_registry = tool_registry
        self.provider = provider
        self.max_iterations = max_iterations

    def run(self, task: str) -> AgentResult:

        # Conversation state for this agent run.
        context = ContextManager()
        context.add_user_message(task)

        # Store a structured execution trace.
        steps = []

        for iteration in range(self.max_iterations):
            print(
                f"\n--- Iteration "
                f"{iteration + 1} ---"
            )

            print("Calling Gemini...")

            response = self.provider.generate(
                contents=context.get_contents(),
                tools=[
                    self.tool_registry.to_gemini_tool()
                ],
                system_instruction=SYSTEM_INSTRUCTION,
            )

            print("Gemini responded.")

            model_content = (
                response.candidates[0].content
            )

            print("Model parts:")

            for part in model_content.parts:
                print(
                    "  text=",
                    bool(part.text),
                    "function_call=",
                    bool(part.function_call),
                )

            # Add Gemini's response to the conversation.
            context.add_model_message(model_content)

            # Extract all function calls from this response.
            tool_calls = [
                part.function_call
                for part in model_content.parts
                if part.function_call
            ]

            # No tool call means Gemini has finished.
            if not tool_calls:

                final_text = "\n".join(
                    part.text
                    for part in model_content.parts
                    if part.text
                )

                return AgentResult(
                    final_response=final_text,
                    steps=steps,
                )

            tool_results = []

            # Execute every tool requested by Gemini.
            for function_call in tool_calls:

                print("\nTOOL CALL:")
                print(
                    "  name:",
                    function_call.name,
                )
                print(
                    "  args:",
                    function_call.args,
                )

                result = (
                    self.tool_registry.execute(
                        function_call.name,
                        **function_call.args,
                    )
                )

                print(
                    "TOOL RESULT:",
                    result,
                )

                # Store the execution in our trace.
                steps.append(
                    AgentStep(
                        iteration=iteration + 1,
                        tool_name=function_call.name,
                        arguments=dict(
                            function_call.args
                        ),
                        result=result,
                    )
                )

                # Convert the Python result into
                # a Gemini function-response part.
                tool_results.append(
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={
                            "tool_result": result
                        },
                    )
                )

            print(
                "Sending tool result back to Gemini..."
            )

            # Send all tool results back to Gemini.
            context.add_tool_results(tool_results)
        # Agent reached its iteration limit.
        return AgentResult(
            final_response=(
                "Agent stopped because it reached "
                f"the maximum of "
                f"{self.max_iterations} iterations."
            ),
            steps=steps,
        )
