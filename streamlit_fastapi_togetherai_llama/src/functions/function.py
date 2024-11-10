def download_and_clean_html(url):
    response = requests.get(url)
    cleaned_html = remove_script_css(response.content)
    return cleaned_html

from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure, log
from llama_index.core.llms import ChatMessage, MessageRole
import os
from dataclasses import dataclass
import requests

# from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src.functions.utils.clean_div import remove_script_css

load_dotenv()


@dataclass
class FunctionInputParams:
    prompt: str


@function.defn(name="llm_complete")
async def llm_complete(input: FunctionInputParams):
    try:
        log.info("llm_complete function started", input=input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")

        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
        )
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this llm_complete function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM,
                content="You are a pirate with a colorful personality",
            ),
            ChatMessage(role=MessageRole.USER, content=input.prompt),
        ]
        resp = llm.chat(messages)

        # Download and parse the URL
        url = "https://docs.llamaindex.ai/en/stable/examples/llm/together/"
        response = requests.get(url)
        # soup = BeautifulSoup(response.content, "html.parser")
        # parsed_content = soup.get_text()
        # Clean up the HTML content

        cleaned_html = remove_script_css(response.content)

        log.info(
            "llm_complete function completed",
            response=resp.message.content,
            parsed_content=cleaned_html,
            # parsed_content=parsed_content,
        )
        # return resp.message.content + "\n\nParsed Content:\n" + parsed_content
        # return resp.message.content + "\n\nParsed Content:\n" + cleaned_html
        return resp.message.content + "\n\nParsed Content:\n" + cleaned_html
    except Exception as e:
        log.error("llm_complete function failed", error=e)
        raise e
