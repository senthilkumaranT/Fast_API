import streamlit as st
import requests
import json

# FastAPI endpoint URL
API_URL = "http://localhost:8000"

st.title("DocLing Document QA System")

# Chat section
st.header("Ask Questions")
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your document"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request
    collection_name = "bitcoin"  # Set your predefined collection name here
    data = {
        "collection_name": collection_name,
        "question": prompt,
        "limit": 5
    }

    try:
        # Make request to FastAPI endpoint
        response = requests.post(f"{API_URL}/chat/stream", json=data)
        
        # Display assistant response
        with st.chat_message("assistant"):
            if response.status_code == 200:
                response_text = response.json()
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error("Error getting response from server")
    except Exception as e:
        st.error(f"Error: {str(e)}")
