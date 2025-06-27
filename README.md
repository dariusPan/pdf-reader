# GPT PDF Uploader

A Streamlit web app to chat with your PDF by uploading it directly to OpenAI for AI-powered Q&A.

---

## Features

- Upload any PDF file
- Powered by OpenAI’s Assistants API (file Q&A support)
- Simple, modern UI (Streamlit)

---

## Installation

1. **Clone the repo**
    ```
    git clone https://github.com/yourusername/gpt-pdf-uploader.git
    cd gpt-pdf-uploader
    ```
2. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```
3. **Set your OpenAI API key**
    - Copy `.env.example` to `.env` and fill in your key:
      ```
      OPENAI_API_KEY=sk-...
      ```
4. **Run the app**
    ```
    streamlit run app.py
    ```

---

## Usage

1. Upload a PDF.
2. Ask any question.
3. Get answers from GPT, referencing your PDF.

---

## Notes

- Requires OpenAI API access (with Assistants API and file Q&A support).
- For multi-turn chat, the conversation is persisted per session.

---
