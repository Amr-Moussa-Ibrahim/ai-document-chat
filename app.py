"""
app.py
======
The web app you actually see and click on.

Run it with:   streamlit run app.py

It gives you a browser page where you can upload a PDF/TXT file and chat with it.
All the AI logic lives in the `src/` folder; this file is just the interface.
"""

import tempfile
from pathlib import Path

import streamlit as st

from src.chatbot import DocumentChatbot


# --------------------------------------------------------------------------- #
# Page setup
# --------------------------------------------------------------------------- #
st.set_page_config(page_title="AI Document Chat", page_icon="🤖", layout="wide")
st.title("🤖 AI Document Chat")
st.caption(
    "Upload a document and ask questions about it. "
    "100% free & offline — no API keys, powered by open-source AI models."
)


# --------------------------------------------------------------------------- #
# Load the chatbot once and keep it in memory between clicks (session state).
# The @st.cache_resource decorator makes sure the AI models load only ONCE.
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner="Loading AI models (first run downloads them)...")
def get_chatbot() -> DocumentChatbot:
    return DocumentChatbot()


bot = get_chatbot()

# Remember chat history and whether a doc was loaded, across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False


# --------------------------------------------------------------------------- #
# Sidebar: upload documents
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.header("📄 Your documents")
    uploaded = st.file_uploader(
        "Upload a PDF, TXT or MD file",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )

    if uploaded and st.button("Add to knowledge base", type="primary"):
        total_chunks = 0
        for file in uploaded:
            # Save the uploaded file to a temporary path so our loader can read it.
            suffix = Path(file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.getbuffer())
                tmp_path = tmp.name
            with st.spinner(f"Reading and indexing {file.name}..."):
                total_chunks += bot.add_file(tmp_path)
        st.session_state.doc_loaded = True
        st.success(f"Done! Indexed {total_chunks} text chunks. Ask me anything 👇")

    st.divider()
    st.markdown(
        "**How it works**\n\n"
        "1. Your file is split into small chunks.\n"
        "2. Each chunk is turned into an *embedding* (numbers that capture meaning).\n"
        "3. Your question finds the most relevant chunks.\n"
        "4. A free AI model writes an answer from those chunks (this is **RAG**)."
    )


# --------------------------------------------------------------------------- #
# Main area: the chat
# --------------------------------------------------------------------------- #

# Show the conversation so far.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources used for this answer"):
                for i, (chunk, score) in enumerate(msg["sources"], start=1):
                    st.markdown(f"**Match {i}** (similarity {score:.2f})")
                    st.write(chunk)

# Chat input box at the bottom.
question = st.chat_input("Ask a question about your document...")

if question:
    # Show the user's message.
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate and show the assistant's answer.
    with st.chat_message("assistant"):
        if not st.session_state.doc_loaded:
            answer = "Please upload a document in the sidebar first 🙂"
            sources = []
            st.markdown(answer)
        else:
            with st.spinner("Thinking..."):
                answer, sources = bot.ask(question)
            st.markdown(answer)
            if sources:
                with st.expander("📚 Sources used for this answer"):
                    for i, (chunk, score) in enumerate(sources, start=1):
                        st.markdown(f"**Match {i}** (similarity {score:.2f})")
                        st.write(chunk)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
