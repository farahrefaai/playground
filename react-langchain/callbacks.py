from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Any, Dict
from langchain_core.outputs.llm_result import LLMResult


class AgentCallBackHandler(BaseCallbackHandler):
    """Callback handler for agent execution."""

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """
        Run when LLM starts running.
        """
        for prompt in prompts:
            print(f"***Prompt to LLM was:***\n{prompt}")
            print("*********")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """
        Run when LLM ends running.
        """
        print(f"***LLM Response:***\n{response.generations[0][0].text}")
        print("*********")
