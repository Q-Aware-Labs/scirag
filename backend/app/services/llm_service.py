"""
LLM Service
Abstraction layer for multiple LLM providers (Claude, OpenAI, DeepSeek, Gemini)
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, api_key: str, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model or self.get_default_model()

    @abstractmethod
    def get_default_model(self) -> str:
        """Return the default model for this provider"""
        pass

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate a response from the LLM"""
        pass


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider"""

    def get_default_model(self) -> str:
        return "claude-sonnet-4-20250514"

    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise ValueError(f"Failed to generate response from Claude: {str(e)}")


class OpenAIProvider(LLMProvider):
    """OpenAI provider (GPT models)"""

    def get_default_model(self) -> str:
        return "gpt-4o"

    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise ValueError(f"Failed to generate response from OpenAI: {str(e)}")


class DeepSeekProvider(LLMProvider):
    """DeepSeek provider"""

    def get_default_model(self) -> str:
        return "deepseek-chat"

    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            from openai import OpenAI

            # DeepSeek uses OpenAI-compatible API
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            raise ValueError(f"Failed to generate response from DeepSeek: {str(e)}")


class GeminiProvider(LLMProvider):
    """Google Gemini provider"""

    def get_default_model(self) -> str:
        return "gemini-1.5-pro"

    def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)

            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise ValueError(f"Failed to generate response from Gemini: {str(e)}")


class LLMService:
    """Service for managing LLM providers"""

    PROVIDERS = {
        "claude": ClaudeProvider,
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "gemini": GeminiProvider,
    }

    @staticmethod
    def create_provider(provider_name: str, api_key: str, model: Optional[str] = None) -> LLMProvider:
        """
        Create an LLM provider instance

        Args:
            provider_name: Name of the provider (claude, openai, deepseek, gemini)
            api_key: API key for the provider
            model: Optional specific model to use

        Returns:
            LLMProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        if provider_name not in LLMService.PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider_name}. "
                f"Supported providers: {', '.join(LLMService.PROVIDERS.keys())}"
            )

        provider_class = LLMService.PROVIDERS[provider_name]
        return provider_class(api_key=api_key, model=model)

    @staticmethod
    def get_supported_providers() -> Dict[str, str]:
        """Return a dict of supported providers and their default models"""
        return {
            name: provider_class(api_key="dummy").get_default_model()
            for name, provider_class in LLMService.PROVIDERS.items()
        }
