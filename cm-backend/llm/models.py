from abc import abstractmethod, ABC
from typing import Dict

import tiktoken
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer


class BaseLLM(ABC):
    """Wrapper class for the LLM used for concept map extraction."""

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def generate(self, prompt: ChatPromptTemplate, params: Dict[str, str], parser: BaseOutputParser = None):
        """Takes a prompt-template and a dictionary of parameters completing the prompt and generates the output of
        the llm."""

        if parser:
            chain = prompt | self.llm | parser
        else:
            chain = prompt | self.llm

        message = chain.invoke(params)
        return message

    @abstractmethod
    async def num_tokens_from_string(self, string: str) -> str:
        """Given a string returns the number of tokens the given string consists of"""

    @abstractmethod
    async def max_allowed_token_length(self) -> int:
        """Returns the maximum number of tokens the LLM can handle"""


class OpenAiLLM(BaseLLM):
    def __init__(self, openai_api_key: str, model_name: str = "gpt-4o", temp: float = 0.7) -> None:
        llm = ChatOpenAI(
            model=model_name,
            temperature=temp,
            timeout=None,
            max_retries=3,
            api_key=openai_api_key)

        super().__init__(llm)
        self.model_name = model_name

    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def max_allowed_token_length(self) -> int:
        token_limits = {
            "gpt-4o": 30_000,
            "gpt-4o-mini": 128_000,
            "gpt-4-turbo": 30_000,
            "gpt-4": 8_192,
            "gpt-3.5-turbo": 16_385
        }

        if self.model_name in token_limits:
            return token_limits[self.model_name]
        else:
            return 30_000


class MistralAiLLM(BaseLLM):
    def __init__(self, mistral_api_key: str, model_name: str = "mistral-large-latest", temp: float = 0.7) -> None:
        llm = ChatMistralAI(
            model=model_name,
            temperature=temp,
            timeout=240,
            max_retries=3,
            mistral_api_key=mistral_api_key)

        super().__init__(llm)
        self.model_name = model_name

    def num_tokens_from_string(self, string: str) -> int:
        tokenizer = MistralTokenizer.v3()
        tokens = tokenizer.encode_chat_completion(
            ChatCompletionRequest(
                messages=[
                    UserMessage(content=str)
                ],
                model=self.model_name
            )
        ).tokens

        return len(tokens)

    def max_allowed_token_length(self) -> int:
        return 32_768
