# Synth Dev

## Short summary

Helping LLMs understand developer documentation by creating hundreds of diversified use case coding examples for pre-training and RAG.

## Problem

1. AI coding assistants (Copilot, Cursor, Aider.chat) accelerate software development.
2. People typically code not by reading documentation but by asking Llama, ChatGPT, Claude, or other LLMs.
3. LLMs struggle to understand documentation as it requires reasoning.
4. New projects or updated documentation often get overshadowed by legacy code.

## Solution

- To help LLMs comprehend new documentation, we need to generate a large number of usage examples.

## How we do it

1. Download the documentation from the URL and clean it by removing menus, headers, footers, tables of contents, and other boilerplate.
2. Analyze the documentation to extract main ideas, tools, use cases, and target audiences.
3. Brainstorm relevant use cases.
4. Refine each use case.
5. Conduct a human review of the code.
6. Organize the validated use cases into a dataset or RAG system.

## Tools we used

https://github.com/kirilligum/synth-dev

- **Restack**: To run, debug, log, and restart all steps of the pipeline.
- **TogetherAI**: For LLM API and example usage. See: https://github.com/kirilligum/synth-dev/blob/main/streamlit_fastapi_togetherai_llama/src/functions/function.py
- **Llama**: We used Llama 3.2 3b, breaking the pipeline into smaller steps to leverage a more cost-effective model. Scientific research shows that creating more data with smaller models is more efficient than using larger models. See: https://github.com/kirilligum/synth-dev/blob/main/streamlit_fastapi_togetherai_llama/src/functions/function.py
- **LlamaIndex**: For LLM calls, prototyping, initial web crawling, and RAG. See: https://github.com/kirilligum/synth-dev/blob/main/streamlit_fastapi_togetherai_llama/src/functions/function.py




## Running the app:

### Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Together AI](https://together.ai) account with API key

### Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/engine:main
   ```

2. Open the Web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/examples/fastapi_togetherai_llama
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your Together AI API key:

   ```bash
   cp .env.example .env
   # Edit .env and add your TOGETHER_API_KEY
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run fastapi app:

   ```bash
   poetry run app
   ```

8. In a new terminal, run the streamlit frontend

   ```bash
   poetry run streamlit run frontend.py
   ```

9. You can test api endpoint without the streamlit UI with:

   ```bash
   curl -X POST \
     http://localhost:8000/api/schedule \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me a short joke"}'
   ```
