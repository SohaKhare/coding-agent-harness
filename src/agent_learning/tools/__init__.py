from ..registry import ToolRegistry
from ..tool import Tool

from .filesystem import (
    list_files,
    read_file,
    write_file,
    edit_file,
    search_files,
)

from .shell import run_command


def create_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    registry.register(
        Tool(
            name="list_files",
            description=(
                "Lists files and directories "
                "inside the workspace."
            ),
            function=list_files,
        )
    )

    registry.register(
        Tool(
            name="read_file",
            description=(
                "Reads and returns the contents "
                "of a file inside the workspace."
            ),
            function=read_file,
        )
    )

    registry.register(
        Tool(
            name="write_file",
            description=(
                "Creates or overwrites a file "
                "inside the workspace with the "
                "provided content."
            ),
            function=write_file,
        )
    )

    registry.register(
        Tool(
            name="edit_file",
            description=(
                "Edits a file by replacing one "
                "specific piece of text with new text. "
                "The old text must uniquely identify "
                "the section being changed."
            ),
            function=edit_file,
        )
    )

    registry.register(
        Tool(
            name="search_files",
            description=(
                "Searches for text inside files "
                "in the workspace and returns "
                "matching file paths and line numbers."
            ),
            function=search_files,
        )
    )

    registry.register(
        Tool(
            name="run_command",
            description=(
                "Executes an allowed shell command inside the workspace. "
                "Use this when you need to actually run or test code. "
                "Reading a file does not verify that code executes correctly. "
                "Commands may be rejected by the execution policy."
            ),
            function=run_command,
        )
    )

    return registry