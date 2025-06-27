import streamlit as st
import openai
import os
from dotenv import load_dotenv
from utils.pdf_utils import extract_text_from_pdf

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="GPT PDF Reader", page_icon="📄", layout="wide")
st.title("📄 GPT PDF Reader (Text Extractor Version)")
st.write("Upload your PDF, enter a prompt, and chat with its content!")

custom_prompt = st.text_area(
    "Optional system prompt for GPT (influences assistant behavior):",
    value="You are a helpful assistant for reading and summarizing PDF documents.",
    help="For example: 'Answer as an expert lawyer.' Leave as default for a general assistant."
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    if not pdf_text.strip():
        st.error("No extractable text found in this PDF.")
        st.stop()
    st.success("PDF loaded. You can now ask questions about your document!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": custom_prompt},
            {"role": "user", "content": "The following is the text from the PDF document:\n\n" + pdf_text}
        ]

    # Optionally allow the user to reset the conversation
    if st.button("Reset Conversation"):
        st.session_state["messages"] = [
            {"role": "system", "content": custom_prompt},
            {"role": "user", "content": "The following is the text from the PDF document:\n\n" + pdf_text}
        ]

    question = st.text_input("Ask a question about your PDF (or type 'summarize'):")

    if st.button("Submit") and question:
        with st.spinner("GPT is thinking..."):
            st.session_state["messages"].append({"role": "user", "content": question})
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state["messages"],
                max_tokens=700,
                temperature=0.2
            )
            answer = response.choices[0].message.content
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.markdown(f"**Answer:** {answer}")


    # Show conversation history
    if len(st.session_state["messages"]) > 2:
        st.subheader("Conversation History")
        for m in st.session_state["messages"][2:]:
            role = "You" if m["role"] == "user" else "Assistant"
            st.markdown(f"**{role}:** {m['content']}")

else:
    st.info("Please upload a PDF file to get started.")
