from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        contents,
        tools=None,
        system_instruction=None,
    ):
        pass