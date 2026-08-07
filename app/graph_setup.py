from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END


# ============================================================
# GRAPH STATE
# ============================================================

class GraphState(TypedDict):
    query: str
    vectorstore: object
    chat_history: list
    doc_summary: Optional[str]
    response: str


# ============================================================
# START NODE
# ============================================================

def start_node(state: GraphState):
    """
    Initialize the document Q&A workflow.
    """

    return {
        **state,
        "response": ""
    }


# ============================================================
# ANSWER NODE
# ============================================================

def answer_node(state: GraphState):
    """
    Generate an answer using the uploaded documents.
    """

    from app.utils import generate_response

    response = generate_response(
        query=state["query"],
        vectorstore=state["vectorstore"],
        chat_history=state.get("chat_history", []),
        doc_summary=state.get("doc_summary")
    )

    return {
        **state,
        "response": response
    }


# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph():

    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node(
        "start",
        start_node
    )

    workflow.add_node(
        "answer",
        answer_node
    )

    # Entry point
    workflow.set_entry_point(
        "start"
    )

    # Workflow
    workflow.add_edge(
        "start",
        "answer"
    )

    workflow.add_edge(
        "answer",
        END
    )

    # Compile
    return workflow.compile()


# ============================================================
# CREATE GRAPH
# ============================================================

graph = build_graph()