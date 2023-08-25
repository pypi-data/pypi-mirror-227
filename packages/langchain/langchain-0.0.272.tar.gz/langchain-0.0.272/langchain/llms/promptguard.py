import logging
from typing import Any, Dict, List, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.pydantic_v1 import Extra, root_validator
from langchain.schema.language_model import BaseLanguageModel
from langchain.utils import get_from_dict_or_env

logger = logging.getLogger(__name__)


class PromptGuard(LLM):
    """An LLM wrapper that uses PromptGuard to sanitize prompts.

    Wraps another LLM and sanitizes prompts before passing it to the LLM, then
        de-sanitizes the response.

    To use, you should have the ``promptguard`` python package installed,
    and the environment variable ``PROMPTGUARD_API_KEY`` set with
    your API key, or pass it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain.llms import PromptGuard
            from langchain.chat_models import ChatOpenAI

            prompt_guard_llm = PromptGuard(base_llm=ChatOpenAI())
    """

    base_llm: BaseLanguageModel
    """The base LLM to use."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validates that the PromptGuard API key and the Python package exist."""
        try:
            import promptguard as pg
        except ImportError:
            raise ImportError(
                "Could not import the `promptguard` Python package, "
                "please install it with `pip install promptguard`."
            )
        if pg.__package__ is None:
            raise ValueError(
                "Could not properly import `promptguard`, "
                "promptguard.__package__ is None."
            )

        api_key = get_from_dict_or_env(
            values, "promptguard_api_key", "PROMPTGUARD_API_KEY", default=""
        )
        if not api_key:
            raise ValueError(
                "Could not find PROMPTGUARD_API_KEY in the environment. "
                "Please set it to your PromptGuard API key."
                "You can get it by creating an account on the PromptGuard website: "
                "https://promptguard.opaque.co/ ."
            )
        return values

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call base LLM with sanitization before and de-sanitization after.

        Args:
            prompt: The prompt to pass into the model.

        Returns:
            The string generated by the model.

        Example:
            .. code-block:: python

                response = prompt_guard_llm("Tell me a joke.")
        """
        import promptguard as pg

        _run_manager = run_manager or CallbackManagerForLLMRun.get_noop_manager()

        # sanitize the prompt by replacing the sensitive information with a placeholder
        sanitize_response: pg.SanitizeResponse = pg.sanitize(prompt)
        sanitized_prompt_value_str = sanitize_response.sanitized_text

        # TODO: Add in callbacks once child runs for LLMs are supported by LangSmith.
        # call the LLM with the sanitized prompt and get the response
        llm_response = self.base_llm.predict(
            sanitized_prompt_value_str,
            stop=stop,
        )

        # desanitize the response by restoring the original sensitive information
        desanitize_response: pg.DesanitizeResponse = pg.desanitize(
            llm_response,
            secure_context=sanitize_response.secure_context,
        )
        return desanitize_response.desanitized_text

    @property
    def _llm_type(self) -> str:
        """Return type of LLM.

        This is an override of the base class method.
        """
        return "promptguard"
