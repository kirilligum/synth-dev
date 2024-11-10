import streamlit as st
import requests

# Set page title and header
st.title("Synth Dev")

# Create text area for user input with session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
    st.session_state.url_input = ""

url = st.text_area(
    "Enter the URL of your development documentation",
    height=96,
    key="url_input",
    value="https://docs.llamaindex.ai/en/stable/examples/llm/together/",
)
user_prompt = st.text_area(
    "Prompt for the additional requests. For example, focusing on a specific usecase or library or target audience",
    height=150,
    key="user_input",
)

# Initialize response history in session state
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Create button to send request
if st.button("Generate Examples"):
    if user_prompt:
        try:
            # Make POST request to FastAPI backend
            response = requests.post(
                "http://localhost:8000/api/schedule",
                json={"prompt": user_prompt, "url": url},
            )

            if response.status_code == 200:
                st.success("Response received!")
                # Add the new response to history with the original prompt
                st.session_state.response_history.append({
                    "prompt": user_prompt,
                    "url": url,
                    "response": response.json()["result"],
                })
            else:
                st.error(f"Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Failed to connect to the server. Make sure the FastAPI server is running."
            )
    else:
        st.warning("Please enter a prompt before submitting.")

# Display response history
if st.session_state.response_history:
    st.subheader("Response History")
    for i, item in enumerate(st.session_state.response_history, 1):
        st.markdown(f"**Prompt {i}:** {item['prompt']}")
        st.markdown(f"**Response {i}:** {item['response']}")
        st.markdown("---")

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

st.h1("RAG")
st.write("RAG:", st.session_state.rag)
