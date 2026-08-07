from langchain.prompts import ChatPromptTemplate

from app.llm_setup import llm
from app.rag_setup import retrieve


# ============================================================
# DOCUMENT SUMMARY
# ============================================================

def set_summary(text: str) -> str:
    """
    Generate a concise summary of the uploaded documents.
    """

    if not text or not text.strip():
        return "No readable text was found in the uploaded document."

    prompt = ChatPromptTemplate.from_template(
        """
You are a professional document analysis assistant.

Summarize the provided document in 4-6 clear sentences.

Include:
- What the document is about
- Its main purpose
- Important topics
- Important facts or points

Do not add information that is not present in the document.

Document:
{document}

Summary:
"""
    )

    formatted_prompt = prompt.format_messages(
        document=text[:10000]
    )

    response = llm.invoke(formatted_prompt)

    return response.content.strip()


# ============================================================
# DOCUMENT Q&A
# ============================================================

def generate_response(
    query: str,
    vectorstore,
    chat_history=None,
    doc_summary=None
) -> str:
    """
    Generate an answer based ONLY on the uploaded documents.

    If relevant information cannot be found in the documents,
    the assistant clearly says so instead of hallucinating.
    """

    if not query or not query.strip():
        return "Please enter a question."

    query = query.strip()

    if chat_history is None:
        chat_history = []

    # ========================================================
    # DOCUMENT SUMMARY REQUEST
    # ========================================================

    summary_keywords = [
        "summary",
        "summarize",
        "summarise",
        "what is this document",
        "what is this file",
        "what's this document",
        "what's this file",
        "tell me about this document",
        "tell me about this file",
        "explain this document",
        "explain this file",
    ]

    normalized_query = query.lower()

    # Handle common typo
    normalized_query = normalized_query.replace(
        "fike",
        "file"
    )

    is_summary_request = any(
        keyword in normalized_query
        for keyword in summary_keywords
    )

    if is_summary_request:

        if doc_summary:

            return (
                "### 📄 Document Summary\n\n"
                f"{doc_summary}"
            )

        return (
            "I don't have a document summary yet. "
            "Please upload a document first."
        )

    # ========================================================
    # CHAT HISTORY
    # ========================================================

    history_text = "No previous conversation."

    if chat_history:

        history_parts = []

        for sender, message in chat_history:

            if sender == "You":

                history_parts.append(
                    f"User: {message}"
                )

            else:

                history_parts.append(
                    f"Assistant: {message}"
                )

        history_text = "\n".join(
            history_parts
        )

    # ========================================================
    # RETRIEVE DOCUMENT CHUNKS
    # ========================================================

    context_docs = retrieve(
        query,
        vectorstore,
        k=5
    )

    # ========================================================
    # NO RELEVANT DOCUMENTS
    # ========================================================

    if not context_docs:

        return (
            "I couldn't find relevant information "
            "in the uploaded documents to answer "
            "this question."
        )

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    context_parts = []

    for index, doc in enumerate(context_docs, start=1):

        source = doc.metadata.get(
            "source",
            "Unknown document"
        )

        page = doc.metadata.get(
            "page"
        )

        if page is not None:

            page_number = page + 1

            source_text = (
                f"{source}, Page {page_number}"
            )

        else:

            source_text = source

        context_parts.append(
            f"""
SOURCE {index}:
Document: {source_text}

Content:
{doc.page_content}
"""
        )

    context = "\n".join(
        context_parts
    )

    # ========================================================
    # RAG PROMPT
    # ========================================================

    prompt = ChatPromptTemplate.from_template(
        """
You are a professional AI Document Assistant.

Your job is to answer the user's question using
ONLY the information contained in the uploaded
document context.

IMPORTANT RULES:

1. Use the provided document context as the primary
   and only source of factual information.

2. DO NOT use your general knowledge to invent
   information.

3. If the answer is not available in the provided
   documents, say:

   "I couldn't find this information in the uploaded documents."

4. Do not guess.

5. If the user asks a question that requires
   information not contained in the documents,
   clearly explain that the documents do not contain
   the required information.

6. Keep the answer natural and easy to understand.

7. Use bullet points or numbered lists when useful.

8. If the document contains a direct answer,
   answer directly instead of unnecessarily
   repeating the entire document.

9. When appropriate, mention the source document
   and page number.

Conversation History:
{chat_history}

Uploaded Document Context:
{context}

User Question:
{question}

Answer:
"""
    )

    formatted_prompt = prompt.format_messages(
        chat_history=history_text,
        context=context,
        question=query
    )

    # ========================================================
    # CALL LLM
    # ========================================================

    response = llm.invoke(
        formatted_prompt
    )

    answer = response.content.strip()

    # ========================================================
    # SOURCE LIST
    # ========================================================

    sources = []

    for doc in context_docs:

        source = doc.metadata.get(
            "source",
            "Unknown document"
        )

        page = doc.metadata.get(
            "page"
        )

        if page is not None:

            source_label = (
                f"{source}, Page {page + 1}"
            )

        else:

            source_label = source

        if source_label not in sources:

            sources.append(
                source_label
            )

    # ========================================================
    # ADD SOURCES TO RESPONSE
    # ========================================================

    if sources:

        answer += "\n\n### 📚 Sources\n"

        for source in sources:

            answer += f"- 📄 {source}\n"

    return answer