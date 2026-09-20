from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .agent import Agent


@dataclass
class EvalCase:
    name: str
    task: str
    check: Callable[[Path], bool]
    cleanup: list[str]


@dataclass
class EvalResult:
    name: str
    passed: bool
    final_response: str
    iterations: int
    tools_used: list[str]
    error: str | None = None


class Evaluator:

    def __init__(self, agent: Agent, workspace: Path):
        self.agent = agent
        self.workspace = workspace

    def run_case(self, case: EvalCase) -> EvalResult:

        try:

            # Clean files from previous runs.
            for filename in case.cleanup:
                path = self.workspace / filename

                if path.exists():
                    path.unlink()

            result = self.agent.run(case.task)

            passed = case.check(self.workspace)

            return EvalResult(
                name=case.name,
                passed=passed,
                final_response=result.final_response,
                iterations=len(result.steps),
                tools_used=[
                    step.tool_name
                    for step in result.steps
                    if step.tool_name
                ],
            )

        except Exception as e:
            return EvalResult(
                name=case.name,
                passed=False,
                final_response="",
                iterations=0,
                tools_used=[],
                error=f"{type(e).__name__}: {e}",
            )

    def run_all(
        self,
        cases: list[EvalCase],
    ) -> list[EvalResult]:

        results = []

        for case in cases:
            results.append(
                self.run_case(case)
            )

        return results