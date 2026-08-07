import os
import sys

import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

from app.rag_setup import setup_chroma
from app.utils import set_summary
from app.graph_setup import graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Document AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 Document AI Assistant")

st.caption(
    "Upload your documents and ask questions using "
    "RAG + LangGraph + OpenAI."
)


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "doc_summary" not in st.session_state:
    st.session_state.doc_summary = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📄 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)


# ============================================================
# CLEAR CHAT
# ============================================================

if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.chat_history = []

    st.sidebar.success(
        "Chat history cleared."
    )


# ============================================================
# DOWNLOAD CHAT
# ============================================================

if st.sidebar.button("💾 Download Chat"):

    if st.session_state.chat_history:

        df = pd.DataFrame(
            st.session_state.chat_history,
            columns=["Sender", "Message"]
        )

        csv_data = df.to_csv(
            index=False
        )

        st.sidebar.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="chat_history.csv",
            mime="text/csv"
        )

    else:

        st.sidebar.warning(
            "No chat history available."
        )


# ============================================================
# PROCESS DOCUMENTS
# ============================================================

if uploaded_files:

    current_file_names = sorted(
        [
            uploaded_file.name
            for uploaded_file in uploaded_files
        ]
    )

    previous_file_names = sorted(
        st.session_state.uploaded_file_names
    )

    # Process only when document selection changes
    if current_file_names != previous_file_names:

        with st.spinner(
            "📚 Processing documents..."
        ):

            os.makedirs(
                "data",
                exist_ok=True
            )

            doc_paths = []

            all_text = ""

            # ------------------------------------------------
            # SAVE AND READ DOCUMENTS
            # ------------------------------------------------

            for uploaded_file in uploaded_files:

                file_path = os.path.join(
                    "data",
                    uploaded_file.name
                )

                # Save file
                with open(
                    file_path,
                    "wb"
                ) as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                doc_paths.append(
                    file_path
                )

                # ------------------------------------------------
                # TXT
                # ------------------------------------------------

                if uploaded_file.type == "text/plain":

                    try:

                        text = uploaded_file.getvalue().decode(
                            "utf-8",
                            errors="ignore"
                        )

                        all_text += (
                            text + "\n"
                        )

                    except Exception as e:

                        st.warning(
                            f"Could not read "
                            f"{uploaded_file.name}: {e}"
                        )

                # ------------------------------------------------
                # PDF
                # ------------------------------------------------

                elif uploaded_file.type == "application/pdf":

                    try:

                        reader = PdfReader(
                            file_path
                        )

                        for page in reader.pages:

                            page_text = (
                                page.extract_text()
                            )

                            if page_text:

                                all_text += (
                                    page_text + "\n"
                                )

                    except Exception as e:

                        st.warning(
                            f"Could not read "
                            f"{uploaded_file.name}: {e}"
                        )

            # ------------------------------------------------
            # CREATE VECTOR DATABASE
            # ------------------------------------------------

            try:

                st.session_state.vectorstore = (
                    setup_chroma(doc_paths)
                )

            except Exception as e:

                st.error(
                    f"Vector database error: {e}"
                )

                st.stop()

            # ------------------------------------------------
            # DOCUMENT SUMMARY
            # ------------------------------------------------

            if all_text.strip():

                try:

                    st.session_state.doc_summary = (
                        set_summary(all_text)
                    )

                except Exception as e:

                    st.warning(
                        f"Summary generation failed: {e}"
                    )

                    st.session_state.doc_summary = None

            # ------------------------------------------------
            # UPDATE FILE LIST
            # ------------------------------------------------

            st.session_state.uploaded_file_names = (
                current_file_names
            )

            # ------------------------------------------------
            # RESET CHAT WHEN DOCUMENTS CHANGE
            # ------------------------------------------------

            st.session_state.chat_history = []

        st.sidebar.success(
            "✅ Documents processed successfully!"
        )


else:

    st.sidebar.info(
        "Upload documents to begin."
    )


# ============================================================
# SHOW DOCUMENT LIST
# ============================================================

if st.session_state.uploaded_file_names:

    st.sidebar.subheader(
        "📚 Uploaded Documents"
    )

    for file_name in (
        st.session_state.uploaded_file_names
    ):

        st.sidebar.write(
            f"📄 {file_name}"
        )


# ============================================================
# DOCUMENT SUMMARY
# ============================================================

if st.session_state.doc_summary:

    with st.expander(
        "📋 Document Summary"
    ):

        st.write(
            st.session_state.doc_summary
        )


# ============================================================
# CHAT HISTORY
# ============================================================

for sender, message in (
    st.session_state.chat_history
):

    with st.chat_message(
        "user"
        if sender == "You"
        else "assistant"
    ):

        st.markdown(
            message
        )


# ============================================================
# CHAT INPUT
# ============================================================

if st.session_state.vectorstore:

    user_input = st.chat_input(
        "Ask a question about your documents..."
    )

    if user_input:

        # ------------------------------------------------
        # USER MESSAGE
        # ------------------------------------------------

        st.session_state.chat_history.append(
            (
                "You",
                user_input
            )
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_input
            )

        # ------------------------------------------------
        # AI RESPONSE
        # ------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking... 🤔"
            ):

                try:

                    result = graph.invoke(
                        {
                            "query": user_input,

                            "vectorstore":
                                st.session_state.vectorstore,

                            # Don't include the current
                            # question twice
                            "chat_history":
                                st.session_state
                                .chat_history[:-1],

                            "doc_summary":
                                st.session_state.doc_summary,

                            "response": ""
                        }
                    )

                    response = result.get(
                        "response",
                        "I couldn't generate a response."
                    )

                except Exception as e:

                    response = (
                        "Sorry, I couldn't process "
                        "your question."
                    )

                    st.error(
                        f"Error: {e}"
                    )

            st.markdown(
                response
            )

        # ------------------------------------------------
        # SAVE AI RESPONSE
        # ------------------------------------------------

        st.session_state.chat_history.append(
            (
                "Bot",
                response
            )
        )


else:

    st.info(
        "👆 Upload a PDF or TXT document "
        "to start chatting."
    )