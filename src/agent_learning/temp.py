from agent_learning.config import client, MODEL
from agent_learning.tools import create_tool_registry
from google.genai import types

registry = create_tool_registry()

config = types.GenerateContentConfig(
    system_instruction="""
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
7. Pay attention to tool errors and recover from them.
8. Do not claim that code works unless you have actually
   verified it.
""",
    tools=[registry.to_gemini_tool()],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Calling Gemini...")

response = client.models.generate_content(
    model=MODEL,
    contents="Create a file called test.py that prints hello world.",
    config=config,
)

print("Gemini responded!")

for part in response.candidates[0].content.parts:
    print(part)