# -----------------------------------------------
# Using Groq API as a model provider
# -----------------------------------------------


from helpers.functional import print_list

from groq import Groq
from groq.types.chat import ChatCompletion

class GroqModelsAPI:
    """
    Using Groq API as a model provider

    Args:
        api_key (str): Groq api key
        **kwargs     : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
    """
    def __init__(self, api_key: str):
        self.client = self.init_client(api_key = api_key)

    
    def init_client(self, api_key: str) -> Groq:
        return Groq(
            api_key = api_key
        )
    

    def generate(
        self, 
        model_name           : str, 
        user_input           : str,
        system_prompt        : str | None = None, 
        return_whole_response: bool = False, 
        **kwargs
    ) -> ChatCompletion | str:
        """
        Invoking an LLM from Groq

        Args:
            model_name           : the name of the LLM required
            user_input           : the input goes to the LLM
            return_whole_response: whether to return the whole response of just the output text
            **kwargs             : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
        """
        messages = self.create_messages(user_input = user_input, system_prompt = system_prompt)

        completion = self.client.chat.completions.create(
            messages = messages,
            model    = model_name,
            stream   = False,
            **kwargs
        )
        
        if return_whole_response:
            return completion
        
        return completion.choices[0].message.content
    

    def stream(
        self, 
        model_name   : str, 
        user_input   : str,
        system_prompt: str | None = None,  
        **kwargs
    ):
        """
        Invoking an LLM from Groq

        Args:
            model_name           : the name of the LLM required
            user_input           : the input goes to the LLM
            return_whole_response: whether to return the whole response of just the output text
            **kwargs             : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
        """
        messages = self.create_messages(user_input = user_input, system_prompt = system_prompt)

        stream = self.client.chat.completions.create(
            messages = messages,
            model    = model_name,
            stream   = True,
            **kwargs
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content
        
    

    
    def create_messages(self, user_input: str, system_prompt: str | None = None) -> list[dict[str, str]]:
        """
        Preparing the inputs for the invoking
        """
        return [
            {
                "role"   : "system",
                "content": system_prompt,
            },
            {
                "role"   : "user",
                "content": user_input
            }
        ]
    