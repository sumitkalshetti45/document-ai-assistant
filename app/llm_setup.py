import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# OPENAI CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


# ============================================================
# VALIDATE API KEY
# ============================================================

if not OPENAI_API_KEY:

    raise ValueError(
        "OPENAI_API_KEY is not configured. "
        "Add it to your .env file locally or "
        "to Render Environment Variables."
    )


# ============================================================
# CREATE LLM
# ============================================================

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.2,
    api_key=OPENAI_API_KEY
)