from typing import Union, List
from .base_textgen import TextGenerator
from ...datamodel import Message, TextGenerationConfig, TextGenerationResponse
from ...utils import cache_request, num_tokens_from_messages
import os
import openai
from dataclasses import asdict

context_lengths = {
    "gpt-35-turbo": 8192,
    "gpt-35-turbo-16k": 16384,
}


class AzureTextGenerator(TextGenerator):
    def __init__(
        self,
        api_key: str = os.environ.get("AZURE_API_KEY", None),
        provider: str = "azure",
        organization: str = None,
        **kwargs,
    ):
        super().__init__(provider=provider)
        if api_key is None:
            raise ValueError(
                "Azure API key is not set. Please set the AZURE_API_KEY environment variable."
            )
        openai.api_key = api_key
        if organization:
            openai.organization = organization
        self.api_key = api_key

    def generate(
            self, messages: Union[List[dict],
                                  str],
            config: TextGenerationConfig = TextGenerationConfig(),
            **kwargs) -> TextGenerationResponse:

        use_cache = config.use_cache
        model = config.model or "gpt-35-turbo-16k"
        prompt_tokens = num_tokens_from_messages(messages)
        max_tokens = max(context_lengths.get(model, 8192) - prompt_tokens - 10, 200)

        oai_config = {
            "engine":"TestTurbo",
            "model": model,
            "temperature": config.temperature,
            "max_tokens": max_tokens,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "n": config.n,
            "messages": messages,
        }
        self.model_name = model
        cache_key_params = (oai_config) | {"messages": messages}
        if use_cache:
            response = cache_request(cache=self.cache, params=cache_key_params)
            if response:
                return TextGenerationResponse(**response)

        oai_response = openai.ChatCompletion.create(**oai_config)

        response = TextGenerationResponse(
            text=[Message(**x.message) for x in oai_response.choices],
            logprobs=[],
            config=oai_config,
            usage=dict(oai_response.usage),
        )
        # if use_cache:
        cache_request(cache=self.cache, params=cache_key_params, values=asdict(response))
        return response

    def count_tokens(self, text) -> int:
        return num_tokens_from_messages(text)