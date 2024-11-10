from datetime import timedelta

from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.function import (
        download_and_clean_html,
        DownloadInputParams,
        understand_documentation,
        InputParams_understand_documentation,
        brainstorm_use_cases,
        InputParams_brainstorm_use_cases,
        extract_use_case,
        InputParams_extract_use_case,
        extract_use_case,
        InputParams_extract_use_case,
        extract_code_and_cli,
        InputParams_extract_code_and_cli,
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

        understand_documentation_result = await workflow.step(
            understand_documentation,
            InputParams_understand_documentation(
                prompt=input["prompt"], cleaned_html=cleaned_html
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info(
            "understand_documentation completed", result=understand_documentation_result
        )

        brainstorm_use_cases_result = await workflow.step(
            brainstorm_use_cases,
            InputParams_brainstorm_use_cases(
                cleaned_html=cleaned_html,
                special_requirements=input["prompt"],
                understand_documentation_result=understand_documentation_result,
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("brainstorm_use_cases completed", result=brainstorm_use_cases_result)

        extract_use_case_results = []
        for i_use_case in range(5):
            extract_use_case_result = await workflow.step(
                extract_use_case,
                InputParams_extract_use_case(
                    cleaned_html=cleaned_html,
                    brainstorm_use_cases_result=brainstorm_use_cases_result,
                    i_use_case=i_use_case,
                ),
                start_to_close_timeout=timedelta(seconds=120),
            )
            log.info(
                f"extract_use_case {i_use_case} completed",
                result=extract_use_case_result,
            )
            extract_use_case_results.append(extract_use_case_result)

        # result = await workflow.step(
        #     create_use_case,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     create_use_case,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     run_use_case,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     reflect,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     act,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     human,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        # result = await workflow.step(
        #     create_rag,
        #     FunctionInputParams(cleaned_html=cleaned_html, use_case=use_case),
        #     start_to_close_timeout=timedelta(seconds=120),
        # )
        # log.info("brainstorm_use_cases completed", result=result)

        code_and_cli_results = []
        for extract_use_case_result in extract_use_case_results:
            code_and_cli_result = await workflow.step(
                extract_code_and_cli,
                InputParams_extract_code_and_cli(extract_use_case_result=extract_use_case_result),
                start_to_close_timeout=timedelta(seconds=60),
            )
            log.info("extract_code_and_cli completed", result=code_and_cli_result)
            code_and_cli_results.append(code_and_cli_result)

        return (
            cleaned_html,
            understand_documentation_result,
            brainstorm_use_cases_result,
            extract_use_case_results,
        )
