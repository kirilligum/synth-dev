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
        with st.expander("usecase"):
            st.text(
                f"**extract_use_case_result {i}:** {item['extract_use_case_results'][0]}"
            )
        st.markdown("---")

st.header("Human review")

st.markdown(
    "Please review the examples and provide feedback on the use cases and code examples"
)
st.markdown("examples for review")

if "use_cases" not in st.session_state:
    st.session_state.use_cases = []

# display use cases
if st.session_state.use_cases:
    st.subheader("Use Cases")
    for i, item in enumerate(st.session_state.use_cases, 1):
        st.markdown(f"**Use Case {i}:** {item['use_case']}")
        st.markdown(f"**Code {i}:** {item['code']}")
        st.markdown("---")

if "approved" not in st.session_state:
    st.session_state.approve = False

if "rag" not in st.session_state:
    st.session_state.rag = "None"

# Create button to send request
if st.button("Approve Examples"):
    st.session_state.approve = True
    st.session_state.rag = "rag.json"
    # if user_prompt:
    #     try:
    #         # Make POST request to FastAPI backend
    #         response = requests.post(
    #             "http://localhost:8000/api/schedule",
    #             json={"prompt": user_prompt, "url": url},
    #         )

    #         if response.status_code == 200:
    #             st.success("Response received!")
    #             # Add the new response to history with the original prompt
    #             st.session_state.response_history.append({
    #                 "prompt": user_prompt,
    #                 "url": url,
    #                 "response": response.json()["result"],
    #             })
    #         else:
    #             st.error(f"Error: {response.status_code}")

    #     except requests.exceptions.ConnectionError:
    #         st.error(
    #             "Failed to connect to the server. Make sure the FastAPI server is running."
    #         )
    # else:
    #     st.warning("Please enter a prompt before submitting.")

# Display the current state of 'approve'
st.write("Approve state:", st.session_state.approve)

st.header("RAG")
st.write("RAG:", st.session_state.rag)
