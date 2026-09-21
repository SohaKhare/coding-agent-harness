from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        contents,
        tools=None,
        system_instruction=None,
    ):
        pass
