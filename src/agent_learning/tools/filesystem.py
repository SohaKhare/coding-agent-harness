from pathlib import Path


# Project root:
# agent-learning/
#
# filesystem.py:
# agent-learning/src/agent_learning/tools/filesystem.py
#
# parents[3] -> agent-learning/

WORKSPACE = (
    Path(__file__).resolve().parents[3]
    / "workspace"
)

WORKSPACE.mkdir(
    parents=True,
    exist_ok=True,
)


def resolve_path(path: str) -> Path:
    """
    Resolve a path relative to the workspace.

    Prevents the agent from accessing files
    outside the workspace.
    """

    target = (
        WORKSPACE / path
    ).resolve()

    if not target.is_relative_to(
        WORKSPACE.resolve()
    ):
        raise ValueError(
            "Path is outside the workspace."
        )

    return target


def list_files(path: str = ".") -> str:
    directory = resolve_path(path)

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {path}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {path}"
        )

    files = []

    for item in sorted(
        directory.iterdir()
    ):
        if item.is_dir():
            files.append(
                f"[DIR]  {item.name}"
            )
        else:
            files.append(
                f"[FILE] {item.name}"
            )

    if not files:
        return "Directory is empty."

    return "\n".join(files)


def read_file(path: str) -> str:
    file_path = resolve_path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not file_path.is_file():
        raise IsADirectoryError(
            f"Not a file: {path}"
        )

    return file_path.read_text(
        encoding="utf-8"
    )


def write_file(
    path: str,
    content: str,
) -> str:

    file_path = resolve_path(path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return (
        f"Successfully wrote {path}"
    )


def edit_file(
    path: str,
    old_text: str,
    new_text: str,
) -> str:

    file_path = resolve_path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not file_path.is_file():
        raise IsADirectoryError(
            f"Not a file: {path}"
        )

    content = file_path.read_text(
        encoding="utf-8"
    )

    occurrences = content.count(
        old_text
    )

    if occurrences == 0:
        raise ValueError(
            f"Could not find the specified "
            f"text in {path}."
        )

    if occurrences > 1:
        raise ValueError(
            f"The specified text appears "
            f"{occurrences} times in {path}. "
            f"Provide more specific text."
        )

    new_content = content.replace(
        old_text,
        new_text,
    )

    file_path.write_text(
        new_content,
        encoding="utf-8",
    )

    return (
        f"Successfully edited {path}"
    )


def search_files(query: str) -> str:
    results = []

    for file_path in WORKSPACE.rglob("*"):

        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )
        except (
            UnicodeDecodeError,
            PermissionError,
        ):
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            if query.lower() in line.lower():

                relative_path = (
                    file_path.relative_to(
                        WORKSPACE
                    )
                )

                results.append(
                    f"{relative_path}:"
                    f"{line_number}: "
                    f"{line.strip()}"
                )

    if not results:
        return (
            f"No matches found for: {query}"
        )

    return "\n".join(results)