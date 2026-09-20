from google.genai import types


MAX_TOOL_OUTPUT_CHARS = 8_000


class ContextManager:

    def __init__(self):
        self.contents: list[types.Content] = []

    def add_user_message(self, text: str):
        self.contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=text)
                ],
            )
        )

    def add_model_message(
        self,
        content: types.Content,
    ):
        self.contents.append(content)

    def add_tool_results(
        self,
        parts: list[types.Part],
    ):
        limited_parts = []

        for part in parts:

            if not part.function_response:
                limited_parts.append(part)
                continue

            response = part.function_response.response

            # Convert the tool response to text so
            # we can control its size.
            response_text = str(response)

            if len(response_text) > MAX_TOOL_OUTPUT_CHARS:
                response_text = (
                    response_text[:MAX_TOOL_OUTPUT_CHARS]
                    + "\n\n"
                    "[Tool output truncated. "
                    "Use a more specific tool call "
                    "to inspect the remaining data.]"
                )

            limited_parts.append(
                types.Part.from_function_response(
                    name=part.function_response.name,
                    response={
                        "tool_result": response_text
                    },
                )
            )

        self.contents.append(
            types.Content(
                role="user",
                parts=limited_parts,
            )
        )

    def get_contents(self):
        return self.contents

    def clear(self):
        self.contents.clear()