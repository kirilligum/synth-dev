from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure, log
from llama_index.core.llms import ChatMessage, MessageRole
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.functions.utils.clean_div import remove_script_css

@dataclass
class InputParams_extract_code_and_cli:
    extract_use_case_result: str


@function.defn(name="extract_code_and_cli")
async def extract_code_and_cli(input: InputParams_extract_code_and_cli):
    try:
        log.info("extract_code_and_cli function started", input=input)
        
        # Extract the longest Python code block
        python_code_blocks = input.extract_use_case_result.split("<python>")
        python_code = max(
            (block.split("</python>")[0].strip() for block in python_code_blocks if "</python>" in block),
            key=len,
            default=""
        )

        # Extract the longest CLI command block
        cli_blocks = input.extract_use_case_result.split("<cli>")
        cli_command = max(
            (block.split("</cli>")[0].strip() for block in cli_blocks if "</cli>" in block),
            key=len,
            default=""
        )

        log.info("extract_code_and_cli function completed", python_code=python_code, cli_command=cli_command)
        return {"python_code": python_code, "cli_command": cli_command}
    except Exception as e:
        log.error("extract_code_and_cli function failed", error=e)
        raise e
from trafilatura import fetch_url, extract

load_dotenv()


@dataclass
class DownloadInputParams:
    url: str


@dataclass
class InputParams_understand_documentation:
    prompt: str
    cleaned_html: str


@dataclass
class InputParams_brainstorm_use_cases:
    cleaned_html: str
    special_requirements: str
    understand_documentation_result: str


@dataclass
class InputParams_extract_use_case:
    cleaned_html: str
    brainstorm_use_cases_result: str
    i_use_case: int


@function.defn(name="download_and_clean_html")
async def download_and_clean_html(input: DownloadInputParams):
    try:
        log.info("download_and_clean_html function started", input=input)
        downloaded = fetch_url(input.url)
        cleaned_html = extract(downloaded)
        # response = requests.get(input.url)
        # cleaned_html = remove_script_css(response.content)
        log.info(
            "download_and_clean_html function completed", cleaned_html=cleaned_html
        )
        return cleaned_html
    except Exception as e:
        log.error("download_and_clean_html function failed", error=e)
        raise e


@function.defn(name="understand_documentation")
async def understand_documentation(input: InputParams_understand_documentation):
    try:
        log.info("understand_documentation function started", input=input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")

        llm = TogetherLLM(
            # model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
            # model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            api_key=api_key,
        )
        instructions_prompt = """
            You will be givend a <instructions/>, <documentation/>, and <special_requirements/>. Read the documentation carefully. Identify core ideas, tools used, use cases, and audiences. Write them out as a json {"ideas":[str],"tools":[str],"use_cases":[str],"audiences":[str]}.
        """
        full_prompt = f"<instructions>{instructions_prompt}</instructions>  <cleaned_html>{input.cleaned_html}</cleaned_html> <special_requirements>{input.prompt}</special_requirements>"
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this understand_documentation function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM,
                content="You are a staff software engineer at a tech company. You are tasked with expanding the example in the documentation by creating more usecases with a correct code that develeopers can use as examples. You write clear well documented code.",
            ),
            ChatMessage(role=MessageRole.USER, content=full_prompt),
        ]
        resp = llm.chat(messages)

        log.info(
            "understand_documentation function completed",
            response=resp.message.content,
        )
        return resp.message.content
    except Exception as e:
        log.error("understand_documentation function failed", error=e)
        raise e


@function.defn(name="brainstorm_use_cases")
async def brainstorm_use_cases(input: InputParams_brainstorm_use_cases):
    try:
        log.info("brainstorm_use_cases function started", input=input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")

        llm = TogetherLLM(
            # model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
            # model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            api_key=api_key,
        )
        instructions_prompt = """
            You will be given <understand_documentation> that has core ideas, tools used, use cases, and audiences. You will also get special_requirements and original sceapped documentation. Your job is to give five high-quality diversified usecases from the examples in documentation, explain why you picked each usecase, and write a python code snippet that will compile for each of them. 
        """
        full_prompt = f"{instructions_prompt}\n<understand_documentation>{input.understand_documentation_result}</understand_documentation>\n<special_requirements>{input.special_requirements}</special_requirements>\n <documentation>{input.cleaned_html}</documentation> "
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this brainstorm_use_cases function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM,
                content="You are a staff software engineer at a tech company. You are tasked with expanding the example in the documentation by creating more usecases with a correct code that develeopers can use as examples. You write clear well documented code.",
            ),
            ChatMessage(role=MessageRole.USER, content=full_prompt),
        ]
        resp = llm.chat(messages)

        log.info(
            "brainstorm_use_cases function completed",
            response=resp.message.content,
        )
        return resp.message.content
    except Exception as e:
        log.error("brainstorm_use_cases function failed", error=e)
        raise e


@function.defn(name="extract_use_case")
async def extract_use_case(input: InputParams_extract_use_case):
    try:
        log.info("extract_use_case function started", input=input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")

        llm = TogetherLLM(
            # model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
            # model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            api_key=api_key,
        )
        use_case_number = input.i_use_case + 1
        instructions_prompt = f"""
            You will be givend a <instructions/>, <documentation/>, and <brainstorm_use_cases_result/>. Read them carefully. Extract the use case {use_case_number} from the brainstorm_use_cases_result. Correct the extracted code and add explanation for as the comments. At the very end, ouput the python code with the comments for this usecase {use_case_number} between <python> and </python> as single piece of python code that compiles and runs on it's own. after <python/>, output a cli command how to run this code between <cli> and </cli>.
        """
        full_prompt = f"<instructions>{instructions_prompt}</instructions>  <cleaned_html>{input.cleaned_html}</cleaned_html>"
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this extract_use_case function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM,
                content="You are a staff software engineer at a tech company. You are tasked with expanding the example in the documentation by creating more usecases with a correct code that develeopers can use as examples. You write clear well documented code.",
            ),
            ChatMessage(role=MessageRole.USER, content=full_prompt),
        ]
        resp = llm.chat(messages)

        log.info(
            "extract_use_case function completed",
            full_prompt=full_prompt,
            response=resp.message.content,
        )
        return resp.message.content
    except Exception as e:
        log.error("extract_use_case function failed", error=e)
        raise e
