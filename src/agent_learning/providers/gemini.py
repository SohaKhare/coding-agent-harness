import time

from google.genai import types
from google.genai import errors
from ..config import client, MODEL
from ..provider import LLMProvider

# How long to wait (in seconds) before retrying
# after a 429 RESOURCE_EXHAUSTED quota error.
QUOTA_WAIT_SECONDS = 80  # 1 min 20 sec

# How many times to retry after a quota error
# before giving up.
MAX_QUOTA_RETRIES = 5


class GeminiProvider(LLMProvider):

    def __init__(
        self,
        model: str = MODEL,
        max_quota_retries: int = MAX_QUOTA_RETRIES,
    ):
        self.model = model
        self.max_quota_retries = max_quota_retries

    def generate(
        self,
        contents,
        tools=None,
        system_instruction=None,
    ):

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        )

        attempts = 0

        while True:

            try:
                return client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

            except errors.ClientError as e:

                # Only handle quota / rate limit errors.
                if e.code != 429:
                    raise

                attempts += 1

                if attempts > self.max_quota_retries:
                    raise RuntimeError(
                        "Gemini API quota has been exhausted. "
                        f"Gave up after {attempts - 1} retries "
                        f"with a {QUOTA_WAIT_SECONDS}s wait. "
                        "Please wait for the quota to reset or "
                        "use a model/project with available quota."
                    ) from e

                print(
                    f"Gemini API quota exhausted (429). "
                    f"Waiting {QUOTA_WAIT_SECONDS}s before "
                    f"retrying "
                    f"(attempt {attempts}/"
                    f"{self.max_quota_retries})..."
                )

                time.sleep(QUOTA_WAIT_SECONDS)