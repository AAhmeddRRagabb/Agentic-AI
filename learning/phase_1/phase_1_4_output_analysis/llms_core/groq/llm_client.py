



from typing import Any

from groq import Groq



class GroqLLMClient:
    """
    Utilizing the Groq LLMs API to build Agentic AI system

    Args:
        - api_key (str): The API key to access Groq
    """
    # ----------------- Init -------------------- #
    def __init__(self, api_key: str) -> None:
        self.client = self.init_client(api_key = api_key)
    
    def init_client(self, api_key: str) -> Groq:
        return Groq(
            api_key = api_key
        )
    # ------------------ Invoking --------------- #
    def generate(
        self,
        model_name     : str,
        query          : str,
        messages       : list[dict[str, str]] | None = None,
        system_prompt  : str             | None = None,
        response_format: dict[str, Any] | None = None,
        **kwargs
    ):
        """
        Invoking an LLM from Groq & Returning the whole output at once

        Args:
            model_name     : the name of the LLM required
            query          : the input goes to the LLM
            messages       : list of given messages [no need for query]
            system_prompt  : the system prompt controlling the model's output
            response_format: the structured response form required from the model
            **kwargs       : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
        """
        if messages is None:
            messages = self.create_messages(user_input = query, system_prompt = system_prompt)

        if response_format:
            kwargs["response_format"] = response_format

        completion = self.client.chat.completions.create(
            messages = messages,
            model    = model_name,
            stream   = False,
            **kwargs
        )

        return completion.choices[0].message.content
    

    def stream(
        self,
        model_name     : str,
        query          : str,
        messages       : list[dict[str, str]] | None = None,
        system_prompt  : str             | None = None,
        response_format: dict[str, Any] | None = None,
        **kwargs
    ):
        """
        Invoking an LLM from Groq & streaming its output

        Args:
            model_name     : the name of the LLM required
            query          : the input goes to the LLM
            messages       : list of given messages [no need for query].
            system_prompt  : the system prompt controlling the model's output
            response_format: the structured response form required from the model
            **kwargs       : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
        """
        if messages is None:
            messages = self.create_messages(user_input = query, system_prompt = system_prompt)

        if response_format:
            kwargs["response_format"] = response_format

        completion = self.client.chat.completions.create(
            messages = messages,
            model    = model_name,
            stream   = True,
            **kwargs
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content

            yield content
    
    # ---------------- Utils ---------------------- #
    def create_messages(self, user_input: str, system_prompt: str | None = None) -> list[dict[str, str]]:
        """
        Preparing the inputs for the invoking
        """
        messages = []
        if system_prompt:
            messages.append({
                "role"   : "system",
                "content": system_prompt
            })

        messages.append(
            {
                "role"   : "user",
                "content": user_input
            }
        )

        return messages 
