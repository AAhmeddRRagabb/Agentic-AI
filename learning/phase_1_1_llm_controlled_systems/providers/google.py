# -----------------------------------------------
# Using Groq API as a model provider
# -----------------------------------------------



from google.genai import types
from google.genai import Client

from google.genai.types import GenerateContentResponse

class GoogleModelsAPI:
    """
    Using Google API as a model provider

    Args:
        api_key (str): Groq api key
        **kwargs     : keyword arguments to control model behavior [temperature - top_p - max_tokens - ...]
    """
    def __init__(self, api_key: str):
        self.client = self.init_client(api_key)
    
    def init_client(self, api_key: str) -> Client:
        return Client(
            api_key = api_key
        )
    
    def generate(self, model_name: str, user_input: str, return_whole_response: bool = False, **kwargs) -> GenerateContentResponse | str:
        """
        Invoking an LLM from Google

        Args:
            model_name           : the name of the LLM required
            user_input           : the input goes to the LLM
            return_whole_response: whether to return the whole response of just the output text
            **kwargs             : keyword arguments to control model behavior [temperature - top_p - output_max_tokens - ...]
        """
        contents = self.get_contents(user_input = user_input)

        response = self.client.models.generate_content(
            model    = model_name,
            contents = contents,
            config   = types.GenerateContentConfig(
                **kwargs
            )
        )

        if return_whole_response:
            return response
        
        return response.text
    
    def stream(
        self, 
        model_name: str, 
        user_input: str, 
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
        contents = self.get_contents(user_input = user_input)

        stream = self.client.models.generate_content_stream(
            model    = model_name,
            contents = contents,
            config   = types.GenerateContentConfig(
                **kwargs
            )
        )
        
        for chunk in stream:
            content = chunk.text

            if content:
                yield content


    def get_contents(self, user_input: str, system_prompt: str | None = None) -> list[types.Content]:
        return [
            types.Content(
                role = "user",
                parts = [
                    types.Part.from_text(text = user_input)
                ]
            )
        ]    
    
   

    
        


    
    
    