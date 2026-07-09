from app.retrieval.retriever import (
    retrieve_text_query,
    retrieve_image_query,
    filter_relevant_chunks,
    format_context
)
from app.generation.generator import (
    generate_answer,
    generate_answer_from_image
)
from app.processing.image_describer import describe_image
from app.ingestion.image_parser import load_image 


BANKING_KEYWORDS = [
    "bank", "sbp", "loan", "finance", "regulation", "policy", "digital", 
    "payment", "aml", "kyc", "credit", "deposit", "account", "transaction",
    "audit", "risk", "compliance", "microfinance", "licensing", "framework",
    "guideline", "sme", "banking", "interest", "capital", "currency", "money"
]

CONVERSATIONAL_KEYWORDS = [
    "last time", "previous", "before", "earlier", "what did i", 
    "what i asked", "what was my last", "remember", "you said", 
    "you told", "again", "repeat", "last question", "what was the last question"
]

GREETINGS = ["hi", "hello", "hey", "how are you", "help"]


def is_banking_query(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in BANKING_KEYWORDS)


def is_conversational_query(query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in CONVERSATIONAL_KEYWORDS)


def run_text_query(query: str, chat_history: list = []) -> dict:
    """
    Final Fixed Version - Memory + Follow-up better handled
    """
    print(f"\nProcessing text query: {query}")

    query_lower = query.lower().strip()

    # 1. Greeting
    if query_lower in GREETINGS:
        return {"query": query, "answer": "greeting", "sources": [], "retrieved_chunks": []}

    # 2. Pure Memory Questions
    if is_conversational_query(query):
        if chat_history:
            last_question = ""
            for msg in reversed(chat_history):
                if msg.get("role") == "user":
                    last_question = msg.get("content", "")
                    break
            if last_question:
                return {
                    "query": query,
                    "answer": f"Your last question was: '{last_question}'",
                    "sources": [],
                    "retrieved_chunks": []
                }
        return {"query": query, "answer": "No previous question found.", "sources": [], "retrieved_chunks": []}

    # 3. Follow-up / More Info Requests (New Logic)
    if any(word in query_lower for word in ["more info", "more detail", "elaborate", "give more", "tell me more", "further", "explain"]):
        # Agar previous question hai toh usi pe aur info do
        if chat_history:
            last_user_query = ""
            for msg in reversed(chat_history):
                if msg.get("role") == "user":
                    last_user_query = msg.get("content", "")
                    break
            if last_user_query:
                query = last_user_query + " " + query   # Combine for better context

    # 4. Banking Check
    if not is_banking_query(query):
        return {
            "query": query,
            "answer": "This is not a banking related question. Please ask about SBP banking regulations and documents.",
            "sources": [],
            "retrieved_chunks": []
        }

    # ================= MAIN RAG FLOW =================
    retrieved_chunks = retrieve_text_query(query)
    relevant_chunks = filter_relevant_chunks(retrieved_chunks, min_score=0.5)

    if not relevant_chunks:
        return {
            "query": query,
            "answer": "This information is not available in the provided SBP documents.",
            "sources": [],
            "retrieved_chunks": []
        }

    context = format_context(relevant_chunks)
    result = generate_answer(query, context, chat_history)

    sources = list(set([chunk["metadata"].get("source", "unknown") for chunk in relevant_chunks]))

    return {
        "query": query,
        "answer": result["answer"],
        "sources": sources,
        "retrieved_chunks": relevant_chunks
    }


# Image Query (no change)
def run_image_query(image_path: str, query: str, chat_history: list = []) -> dict:
    print(f"\nProcessing image query: {query}")

    image = load_image(image_path)
    image_desc = describe_image(image, image_path)
    image_description = image_desc["content"]

    retrieved_chunks = retrieve_image_query(image_description)
    relevant_chunks = filter_relevant_chunks(retrieved_chunks, min_score=0.5) or retrieved_chunks

    context = format_context(relevant_chunks)
    result = generate_answer_from_image(image_description, query, context, chat_history)

    sources = list(set([chunk["metadata"].get("source", "unknown") for chunk in relevant_chunks]))

    return {
        "query": query,
        "answer": result["answer"],
        "image_description": image_description,
        "sources": sources,
        "retrieved_chunks": relevant_chunks
    }