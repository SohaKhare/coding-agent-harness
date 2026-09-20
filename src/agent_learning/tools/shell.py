import subprocess

from .filesystem import WORKSPACE


MAX_OUTPUT_CHARS = 8_000
COMMAND_TIMEOUT = 30


ALLOWED_COMMANDS = {
    "python",
    "python3",
    "pytest",
    "pip",
    "uv",
    "node",
    "npm",
    "git",
}


def get_command_name(command: str) -> str:
    """
    Extract the executable from a command.

    Example:
        python test.py
        -> python
    """
    return command.strip().split()[0].lower()


def validate_command(command: str):
    if not command.strip():
        raise ValueError("Command cannot be empty.")

    command_name = get_command_name(command)

    if command_name not in ALLOWED_COMMANDS:
        raise PermissionError(
            f"Command '{command_name}' is not allowed."
        )


def run_command(command: str) -> str:
    validate_command(command)

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )

    except subprocess.TimeoutExpired:
        return (
            f"Command timed out after "
            f"{COMMAND_TIMEOUT} seconds."
        )

    output = []

    if result.stdout:
        output.append(
            f"STDOUT:\n{result.stdout}"
        )

    if result.stderr:
        output.append(
            f"STDERR:\n{result.stderr}"
        )

    output.append(
        f"EXIT CODE: {result.returncode}"
    )

    final_output = "\n".join(output)

    if len(final_output) > MAX_OUTPUT_CHARS:
        final_output = (
            final_output[:MAX_OUTPUT_CHARS]
            + "\n\n"
            "[Command output truncated.]"
        )

    return final_output