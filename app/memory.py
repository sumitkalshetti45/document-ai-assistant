# ============================================================
# CONVERSATION MEMORY
# ============================================================

def get_chat_history(chat_history):
    """
    Convert Streamlit chat history into a clean text format
    that can be passed to the LLM.
    """

    if not chat_history:
        return "No previous conversation."

    history = []

    for item in chat_history:

        # Make sure the item has sender + message
        if not isinstance(item, (list, tuple)):
            continue

        if len(item) != 2:
            continue

        sender, message = item

        if not message:
            continue

        if sender == "You":

            history.append(
                f"User: {message}"
            )

        elif sender == "Bot":

            history.append(
                f"Assistant: {message}"
            )

        else:

            history.append(
                f"{sender}: {message}"
            )

    if not history:
        return "No previous conversation."

    return "\n".join(history)