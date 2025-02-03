import streamlit as st
import requests
import json

from retrieve import *

# FastAPI endpoint URL
API_URL = "http://localhost:8000"

st.title("DocLing Document QA System")

# File upload section
st.header("Document Upload")
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
collection_name = st.text_input("Collection Name", "default_collection")

if uploaded_file and st.button("Upload Document"):
    # Save the uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Call the upload endpoint (you'll need to implement this in your FastAPI)
    try:
        from upload import upload_pdf
        upload_pdf("temp.pdf", collection_name)
        st.success("Document uploaded successfully!")
    except Exception as e:
        st.error(f"Error uploading document: {str(e)}")

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
