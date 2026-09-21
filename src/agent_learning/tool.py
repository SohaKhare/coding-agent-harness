import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, get_type_hints

from google.genai import types


@dataclass
class Tool:
    name: str
    description: str
    function: Callable[..., Any]

    def call(self, arguments: dict):
        self.validate_arguments(arguments)
        return self.function(**arguments)

    def execute(self, **kwargs):
        return self.call(kwargs)

    def validate_arguments(self, arguments: dict):
        signature = inspect.signature(self.function)
        type_hints = get_type_hints(self.function)

        # Check for unknown arguments
        for name in arguments:
            if name not in signature.parameters:
                raise TypeError(
                    f"Unexpected argument: {name}"
                )

        # Check required arguments
        for name, parameter in signature.parameters.items():
            if (
                parameter.default is inspect.Parameter.empty
                and name not in arguments
            ):
                raise ValueError(
                    f"Missing required argument: {name}"
                )

        # Check types
        for name, value in arguments.items():

            expected_type = type_hints.get(name)

            if expected_type is None:
                continue

            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Argument '{name}' must be "
                    f"{expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

    def get_parameters(self):
        signature = inspect.signature(self.function)
        type_hints = get_type_hints(self.function)

        properties = {}
        required = []

        for param_name, param in signature.parameters.items():

            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            python_type = type_hints.get(param_name, str)

            if python_type is int:
                json_type = "integer"
            elif python_type is float:
                json_type = "number"
            elif python_type is bool:
                json_type = "boolean"
            else:
                json_type = "string"

            properties[param_name] = {
                "type": json_type
            }

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def to_gemini_declaration(self):
        parameters = self.get_parameters()

        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    name: types.Schema(
                        type=info["type"].upper()
                    )
                    for name, info
                    in parameters["properties"].items()
                },
                required=parameters["required"],
            ),
        )
