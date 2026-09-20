from pathlib import Path

from agent_learning.evaluator import EvalCase


def file_exists(
    filename: str,
):
    def check(workspace: Path) -> bool:
        return (workspace / filename).exists()

    return check

def file_contains(filename: str, text: str):
    def check(workspace: Path) -> bool:
        path = workspace / filename

        if not path.exists():
            return False

        return text in path.read_text(
            encoding="utf-8"
        )

    return check

CASES = [

    EvalCase(
        name="create_python_file",
        task=(
            "Create eval_test.py containing "
            "print('evaluation works')."
        ),
        check=file_contains(
            "eval_test.py",
            "evaluation works",
        ),
        cleanup=[
            "eval_test.py",
        ],
    ),

    EvalCase(
        name="create_multiple_files",
        task=(
            "Create eval_a.py containing "
            "print('A') and eval_b.py containing "
            "print('B')."
        ),
        check=lambda workspace: (
            (workspace / "eval_a.py").exists()
            and
            (workspace / "eval_b.py").exists()
        ),
        cleanup=[
            "eval_a.py",
            "eval_b.py",
        ],
    ),
]