import streamlit as st
import requests

# Set page title and header
st.title("Synth Dev 🎹")

st.header("Input Documentation and Requirements")
# Create text area for user input with session state
if "url_input" not in st.session_state:
    st.session_state.url_input = (
        "https://docs.llamaindex.ai/en/stable/examples/llm/together/"
    )
if "user_input" not in st.session_state:
    st.session_state.user_input = (
        """make sure you use both: LlamaIndex and TogetherAI"""
    )

url = st.text_area(
    "Enter the URL of your development documentation",
    height=96,
    key="url_input",
    value=st.session_state.url_input,
)
st.markdown(
    "Our agents will extract useful concepts from the documentation and create use cases."
)
user_prompt = st.text_area(
    "Prompt for the additional requirements. For example, focusing on a specific usecase or library or target audience",
    height=150,
    key="user_input",
    value=st.session_state.user_input,
)

# Initialize response history in session state
if "response_history" not in st.session_state:
    st.session_state.response_history = []

if "clean_html" not in st.session_state:
    st.session_state.clean_html = ""

# Create button to send request
if st.button("Generate Examples"):
    if url:
        try:
            # Make POST request to FastAPI backend
            response = requests.post(
                "http://localhost:8000/api/schedule",
                json={"prompt": user_prompt, "url": url},
            )

            if response.status_code == 200:
                st.success("Response received!")
                st.session_state.clean_html = response.json()["clean_html"]
                # Add the new response to history with the original prompt
                st.session_state.response_history.append({
                    "prompt": user_prompt,
                    "url": url,
                    "understand_documentation_result": response.json()[
                        "understand_documentation_result"
                    ],
                    "brainstorm_use_cases_result": response.json()[
                        "brainstorm_use_cases_result"
                    ],
                    "extract_use_case_results": response.json()[
                        "extract_use_case_results"
                    ],
                    "code_and_cli_results": response.json()["code_and_cli_results"],
                })
            else:
                st.error(f"Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Failed to connect to the server. Make sure the FastAPI server is running."
            )
    else:
        st.warning("Please enter a prompt before submitting.")

if st.session_state.clean_html:
    with st.expander(f"Clean HTML: {st.session_state.clean_html[:50]}"):
        st.text(st.session_state.clean_html)

if "python_code" not in st.session_state:
    st.session_state.python_code = []

if "rag" not in st.session_state:
    st.session_state.rag = []

# Display response history
if st.session_state.response_history:
    st.subheader("Understand Documentation and Brainstorm Use Cases")
    for i, item in enumerate(st.session_state.response_history, 1):
        with st.expander("Understand"):
            st.markdown(
                f"**understand_documentation_result {i}:** {item['understand_documentation_result']}"
            )
        with st.expander("brainstorm"):
            st.markdown(
                f"**brainstorm_use_cases_result {i}:** {item['brainstorm_use_cases_result']}"
            )
        for j in range(5):
            with st.expander(f"usecase {j + 1}"):
                st.text(
                    f"**extract_use_case_result {j + 1}:** {item['extract_use_case_results'][j]}"
                )
            # Add a new expander for code_and_cli_results
            with st.expander("Code and CLI"):
                code_and_cli = item["code_and_cli_results"][j]
                st.markdown("**Python Code:**")
                st.code(code_and_cli["python_code"], language="python")
                st.markdown("**CLI Command:**")
                st.code(code_and_cli["cli_command"], language="bash")
                st.session_state.python_code.append(
                    st.text_area(
                        "Edit",
                        height=256,
                        key=f"code {j}",
                        value=code_and_cli["python_code"],
                    )
                )
                st.session_state.rag.append(False)
                if st.button(f"Submit to RAG {j + 1}"):
                    st.session_state.rag[j] = True
                st.write("Submitted to RAG:", st.session_state.rag[j])
        st.markdown("---")
