# ------------------
# Main Driver
# ------------------


import helpers.functional as F
from helpers.config import get_settings
from helpers.config import GROQ_LLAMA_8b, GEMINI_FLASH_LITE
from helpers.config import PROVIDER_GROQ, PROVIDER_GOOGLE_GENAI
from core import generate, stream

if __name__ == "__main__":
    F.print_title("Starting the APP")
    
    F.print_subtitle("Setup the System")
    settings       = get_settings()
    groq_api_Key   = settings.GROQ_API_KEY
    gooqle_api_Key = settings.GOOGLE_API_KEY
    user_input     = "Tell me about the current trends in Software Engineering field."

    groq_kwargs = {
        "temperature": 0.4,
        "max_tokens" : 512,
        "top_p"      : 0.9
    }

    google_kwargs = {
        "temperature"        : 0.4,
        "max_output_tokens" : 512,
        "top_p"              : 0.9
    }

    print(f"User Input:\n{user_input}")
    print()
    print()

    
    F.print_subtitle("Generating Responses")
    return_whole_response = False
    llama_8b_response = generate(
        provider              = PROVIDER_GROQ,
        api_key               = groq_api_Key,
        model_name            = GROQ_LLAMA_8b,
        user_input            = user_input,
        return_whole_response = return_whole_response,
        **groq_kwargs
    )

    gemini_flash_response = generate(
        provider              = PROVIDER_GOOGLE_GENAI,
        api_key               = gooqle_api_Key,
        model_name            = GEMINI_FLASH_LITE,
        user_input            = user_input,
        return_whole_response = return_whole_response,
        **google_kwargs
    )


    if return_whole_response:
        print(">> Groq LLAMA 8B:")
        print(llama_8b_response.model_dump_json(indent = 4))
        print()
        print(f"Text Response: {llama_8b_response.choices[0].message.content}")
        print()
        print()

    
        print(">> Google Gemini Flash:")
        print(gemini_flash_response.model_dump_json(indent = 4))
        print()
        print(f"Text Response: {gemini_flash_response.text}")

    else:
        print(f">> Groq LLAMA 8B Response:\n{llama_8b_response}")
        print()
        print()
        print(f">> Google Gemini Flash Response:\n{gemini_flash_response}")

    print()
    print()

    F.print_subtitle("Streaming Responses")
    print(">> Groq LLAMA 8B Streaming:")
    for token in stream(
        provider   = PROVIDER_GROQ,
        api_key    = groq_api_Key,
        model_name = GROQ_LLAMA_8b,
        user_input = user_input,
        **groq_kwargs
    ):
        print(token, end = "")


    print()
    print()
    print(">> Google Gemini Flash Streaming:")
    for token in stream(
        provider   = PROVIDER_GOOGLE_GENAI,
        api_key    = gooqle_api_Key,
        model_name = GEMINI_FLASH_LITE,
        user_input = user_input,
        **google_kwargs
    ):
        print(token, end = "")

    print()
    print()
    F.print_title("Finished")
    
    
