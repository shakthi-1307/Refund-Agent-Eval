import os
import asyncio
from openai import OpenAI, AsyncOpenAI
from deepeval.models import DeepEvalBaseLLM


class GroqJudge(DeepEvalBaseLLM):
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise EnvironmentError(
                "GROQ_API_KEY is not set. "
                "Set it in your terminal before running the evaluation."
            )

        # This is a MODEL ID, not your API key.
        self.model_name = "openai/gpt-oss-120b"

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        self.async_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def load_model(self):
        return self.client

    def get_model_name(self):
        return self.model_name

    def generate(self, prompt: str, schema=None) -> str:
        kwargs = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }

        if schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "evaluation_result",
                    "strict": True,
                    "schema": schema.model_json_schema(),
                },
            }

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    async def a_generate(self, prompt: str, schema=None) -> str:
        kwargs = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }

        if schema is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "evaluation_result",
                    "strict": True,
                    "schema": schema.model_json_schema(),
                },
            }

        response = await self.async_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""

    def generate_schema(self, prompt: str, schema):
        return self.generate(prompt, schema=schema)

    async def a_generate_schema(self, prompt: str, schema):
        return await self.a_generate(prompt, schema=schema)


eval_model = GroqJudge()