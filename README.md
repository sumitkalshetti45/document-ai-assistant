# 🤖 Document AI Assistant

An AI-powered document question-answering application built using **Retrieval-Augmented Generation (RAG)**, **LangGraph**, **ChromaDB**, **LangChain**, **OpenAI**, and **Streamlit**.

The application allows users to upload documents and ask questions about their content. It retrieves relevant information from uploaded documents and generates contextual answers using an LLM.

---

## 🚀 Features

- 📄 Upload PDF and TXT documents
- 📚 Support multiple documents
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Context-aware question answering
- 💬 Conversation history
- 📋 Automatic document summary
- 🤖 OpenAI-powered responses
- 🗂️ ChromaDB vector database
- 🔄 LangGraph-based workflow
- 🛡️ Document-grounded responses to reduce hallucinations
- 💾 Download chat history as CSV
- 🌐 Streamlit user interface
- ☁️ Ready for Render deployment

---

## 🏗️ Architecture

```text
                    User
                      │
                      ▼
              ┌───────────────┐
              │   Streamlit   │
              │      UI       │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   LangGraph   │
              │   Workflow    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Retriever   │
              │    ChromaDB   │
              └───────┬───────┘
                      │
                      ▼
              Relevant Context
                      │
                      ▼
              ┌───────────────┐
              │  OpenAI LLM   │
              │  GPT-4o-mini  │
              └───────┬───────┘
                      │
                      ▼
                 Final Answer

🧰 Technologies Used
Programming Language
Python
Generative AI
OpenAI
Large Language Models (LLMs)
Prompt Engineering
Retrieval-Augmented Generation (RAG)
AI Frameworks
LangChain
LangGraph
Vector Database
ChromaDB
Document Processing
PyPDF
PyPDF2
Recursive Character Text Splitter
Frontend
Streamlit
Backend / API
FastAPI
Pydantic
Data & Utilities
Pandas
Python-dotenv


📁 Project Structure
document-ai-assistant/
│
├── app/
│   ├── graph_setup.py
│   ├── llm_setup.py
│   ├── memory.py
│   ├── rag_setup.py
│   └── utils.py
│
├── sapp.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/              # Local uploaded documents
├── chroma_store/      # Local vector database
└── .env               # Local environment variables

data/, chroma_store/, and .env are excluded from GitHub using .gitignore.

🔄 How It Works
1. Upload Documents

Users can upload PDF or TXT files through the Streamlit interface.

PDF / TXT
   ↓
Document Loader
2. Document Processing

The documents are split into smaller chunks using:

RecursiveCharacterTextSplitter

This makes the content easier to search.

3. Create Embeddings

Each document chunk is converted into vector embeddings using OpenAI embeddings.

Document Chunk
      ↓
OpenAI Embeddings
      ↓
Vector Representation
4. Store in ChromaDB

The embeddings are stored in ChromaDB for semantic search.

Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
ChromaDB
5. Retrieve Relevant Information

When the user asks a question, the application searches ChromaDB for relevant document chunks.

User Question
      ↓
Similarity Search
      ↓
Relevant Chunks
6. Generate Answer

The retrieved context is provided to the OpenAI model along with the user's question and conversation history.

Question
   +
Retrieved Context
   +
Chat History
   ↓
OpenAI LLM
   ↓
Answer
💬 Example
User uploads
College_Attendance_Policy.pdf
User asks
What is the minimum attendance requirement?
Application workflow
Question
   ↓
ChromaDB Retrieval
   ↓
Relevant Document Content
   ↓
OpenAI
   ↓
Answer
Example response
The minimum attendance requirement is 75%.

The application is designed to reduce hallucinations by grounding answers in the uploaded documents.

🧠 LangGraph Workflow

The application uses LangGraph to organize the AI workflow.

START
  │
  ▼
Start Node
  │
  ▼
Question Node
  │
  ▼
RAG / LLM Processing
  │
  ▼
Answer Node
  │
  ▼
END

LangGraph provides a structured workflow that can be extended with additional AI agents, tools, and decision-making steps.

⚙️ Installation
1. Clone the repository
git clone https://github.com/sumitkalshetti45/document-ai-assistant.git
2. Navigate into the project
cd document-ai-assistant
3. Create a virtual environment

Windows:

python -m venv env
4. Activate the environment

PowerShell:

.\env\Scripts\Activate.ps1

Windows CMD:

env\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

Never commit your .env file or API key to GitHub.

▶️ Run the Application

Start the Streamlit application:

streamlit run sapp.py

The application will open in your browser.

🧪 Testing

After uploading a document, try questions such as:

What is this document about?
What are the main points?
What are the questions for Assignment Number 3?
Explain this topic in simple language.

You can also ask questions that are not present in the document to test how the application handles missing information.

🔮 Future Improvements
 DOCX document support
 PPTX document support
 Excel and CSV document support
 OCR support for scanned PDFs
 Source citations with page numbers
 Hybrid search
 Reranking
 Improved conversational memory
 Multi-user support
 Authentication
 Persistent cloud vector database
 FastAPI backend integration
 Agentic RAG workflows
 Document comparison
 Improved hallucination detection
👨‍💻 Author

Sumit Kalshetti

B.Tech Information Technology

GitHub: https://github.com/sumitkalshetti45

📄 License

This project is intended for educational and portfolio purposes.
