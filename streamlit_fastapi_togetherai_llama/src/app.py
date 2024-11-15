from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
import time
from restack_ai import Restack
import uvicorn


# Define request model
@dataclass
class PromptRequest:
    prompt: str
    url: str


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return "Welcome to the TogetherAI LlamaIndex FastAPI App!"


@app.post("/api/schedule")
async def schedule_workflow(request: PromptRequest):
    try:
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-llm_complete_workflow"

        runId = await client.schedule_workflow(
            workflow_name="llm_complete_workflow",
            workflow_id=workflow_id,
            input={"url": request.url, "prompt": request.prompt},
        )
        print("Scheduled workflow", runId)

        (
            clean_html,
            understand_documentation_result,
            brainstorm_use_cases_result,
            extract_use_case_results,
            code_and_cli_results,
        ) = await client.get_workflow_result(workflow_id=workflow_id, run_id=runId)
        print(
            "\nclean_html:",
            clean_html[:20],
            "\nunderstand_documentation_result:",
            understand_documentation_result,
            "\nbrainstorm_use_cases_result:",
            brainstorm_use_cases_result,
            "\nextract_use_case_result:",
            extract_use_case_results,
            "\ncode_and_cli_results:",
            code_and_cli_results,
        )

        return {
            "clean_html": clean_html,
            "understand_documentation_result": understand_documentation_result,
            "brainstorm_use_cases_result": brainstorm_use_cases_result,
            "extract_use_case_results": extract_use_case_results,
            "code_and_cli_results": code_and_cli_results,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Remove Flask-specific run code since FastAPI uses uvicorn
def run_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
