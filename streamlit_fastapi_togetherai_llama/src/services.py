import asyncio
from src.client import client
from src.functions.function import (
    download_and_clean_html,
    understand_documentation,
    brainstorm_use_cases,
    extract_use_case,
)
from src.workflows.workflow import llm_complete_workflow


async def main():
    await client.start_service(
        workflows=[llm_complete_workflow],
        functions=[
            download_and_clean_html,
            understand_documentation,
            brainstorm_use_cases,
            extract_use_case,
        ],
    )


def run_services():
    asyncio.run(main())


if __name__ == "__main__":
    run_services()
