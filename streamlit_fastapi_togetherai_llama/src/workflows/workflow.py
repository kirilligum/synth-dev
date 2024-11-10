from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.function import (
        llm_complete,
        download_and_clean_html,
        FunctionInputParams,
        DownloadInputParams,
    )


@workflow.defn(name="llm_complete_workflow")
class llm_complete_workflow:
    @workflow.run
    async def run(self, input: dict):
        log.info("llm_complete_workflow started", input=input)
        # Step 1: Download and clean HTML
        url = "https://docs.llamaindex.ai/en/stable/examples/llm/together/"
        cleaned_html = await workflow.step(
            download_and_clean_html,
            DownloadInputParams(url=url),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("cleaned_html completed", result=cleaned_html)
        prompt = input["prompt"]
        result = await workflow.step(
            llm_complete,
            FunctionInputParams(prompt=prompt),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("llm_complete_workflow completed", result=result)
        return cleaned_html, result
