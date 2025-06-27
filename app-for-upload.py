import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("📄 GPT-4o PDF Reader (Responses API HTTP)")

custom_prompt = st.text_area(
    "System prompt (optional):",
    value="You are a helpful assistant for reading and summarizing PDF documents."
)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

file_id = None

if uploaded_file:
    # Save the PDF locally for upload
    with open("temp_upload.pdf", "wb") as f:
        f.write(uploaded_file.read())
    st.info("Uploading PDF to OpenAI...")

    # --- Step 1: Upload the file to OpenAI (as an 'assistants' file) ---
    with open("temp_upload.pdf", "rb") as file_data:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        files = {
            "file": ("temp_upload.pdf", file_data, "application/pdf")
        }
        data = {
            "purpose": "assistants"
        }
        file_upload_response = requests.post(
            "https://api.openai.com/v1/files",
            headers=headers,
            files=files,
            data=data
        )

    if file_upload_response.status_code != 200:
        st.error(f"File upload failed: {file_upload_response.text}")
        st.stop()

    file_id = file_upload_response.json()["id"]
    st.success(f"PDF uploaded (file ID: {file_id})")

    question = st.text_input("Ask a question about your PDF:")

    if st.button("Submit") and question:
        st.info("Querying GPT-4o with your PDF...")

        # --- Step 2: Call the /v1/responses endpoint directly ---
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "tools": [{"type": "file_search"}],
            "input": [
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": question}
            ],
            "attachments": [
                {"file_id": file_id, "tools": [{"type": "file_search"}]}
            ],
            "max_tokens": 700
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            json=data
        )

        if response.status_code != 200:
            st.error(f"OpenAI API error: {response.text}")
        else:
            try:
                resp_data = response.json()
                # See the structure in the OpenAI docs—adapt as needed!
                answer = resp_data.get("choices", [{}])[0].get("message", {}).get("content")
                if answer:
                    st.markdown(f"**Answer:** {answer}")
                else:
                    st.warning("No answer content found in OpenAI response.")
            except Exception as e:
                st.error(f"Failed to parse OpenAI response: {e}")

else:
    st.info("Please upload a PDF file to get started.")
