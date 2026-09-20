from google.genai import types

from .tool import Tool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self.tools:
            raise KeyError(
                f"Unknown tool: {name}"
            )

        return self.tools[name]

    def list_tools(self):
        return list(self.tools.values())

    def execute(self, name: str, **kwargs):
        try:
            tool = self.get(name)

            result = tool.execute(**kwargs)

            return {
                "success": True,
                "tool": name,
                "result": result,
            }

        except KeyError as e:
            return {
                "success": False,
                "tool": name,
                "error": "UnknownTool",
                "message": str(e),
            }

        except TypeError as e:
            return {
                "success": False,
                "tool": name,
                "error": "InvalidArguments",
                "message": str(e),
            }

        except Exception as e:
            return {
                "success": False,
                "tool": name,
                "error": type(e).__name__,
                "message": str(e),
            }

    def to_gemini_tool(self):
        return types.Tool(
            function_declarations=[
                tool.to_gemini_declaration()
                for tool in self.tools.values()
            ]
        )