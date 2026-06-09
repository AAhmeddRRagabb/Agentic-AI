# ---------------------------------------
# Using models to generate
# ---------------------------------------

from helpers.config     import PROVIDER_GROQ, PROVIDER_GOOGLE_GENAI

from providers.groq     import GroqModelsAPI
from providers.google   import GoogleModelsAPI

from groq.types.chat    import ChatCompletion
from google.genai.types import GenerateContentResponse


def get_llm_api(provider: str, api_key: str) -> GroqModelsAPI | GoogleModelsAPI:
    provider = provider.lower()
    if provider == PROVIDER_GROQ:
        return GroqModelsAPI(api_key = api_key)
    elif provider == PROVIDER_GOOGLE_GENAI:
        return GoogleModelsAPI(api_key = api_key)
    

    raise ValueError(f"Provider name: {provider} is not valid")



def generate(
    provider             : str,
    api_key              : str,
    model_name           : str,
    user_input           : str,
    system_prompt        : str | None = None,
    return_whole_response: bool = False,
    **kwargs
) -> ChatCompletion | GenerateContentResponse | str:
    """
    Abstract function for calling an LLM using these LLM providers:
        - groq
        - google_genai
    
    Args:
        provider             : the name of the provider (groq | google_genai).
        api_key              : the provider api key
        model_name           : the model used in generation
        user_input           : the user input
        return_whole_response: whether to return the whole response of just the output text
        
    Returns:
        response (ChatCompletion | GenerateContentResponse | str)
    """
    llm_api = get_llm_api(provider = provider, api_key = api_key)

    if "stream" in kwargs:
        kwargs.pop("stream")
        
    return llm_api.generate(
        model_name            = model_name,
        user_input            = user_input,
        system_prompt         = system_prompt,
        return_whole_response = return_whole_response,
        **kwargs
    )
    

def stream(
    provider     : str,
    api_key      : str,
    model_name   : str,
    user_input   : str,
    system_prompt: str | None = None,
    **kwargs
):
    """
    Abstract function for streaming a LLM output. Providers should be:
        - groq
        - google_genai
    
    Args:
        provider             : the name of the provider (groq | google_genai).
        api_key              : the provider api key
        model_name           : the model used in generation
        user_input           : the user input
        
    Returns:
        response (ChatCompletion | GenerateContentResponse | str)
    """

    llm_api = get_llm_api(provider = provider, api_key = api_key)

    if "stream" in kwargs:
        kwargs.pop("stream")


    for token in llm_api.stream(
        model_name    = model_name,
        user_input    = user_input,
        system_prompt = system_prompt,
        **kwargs
    ):
        yield token