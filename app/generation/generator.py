from groq import Groq
from app.config.settings import GROQ_API_KEY, GROQ_TEXT_MODEL


def generate_answer(query: str, context: str, chat_history: list = []) -> dict:
    """
    Generate answer using Groq LLaMA model
    Uses chat history for conversation memory
    Returns dict with answer and metadata
    """
    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """You are a helpful banking document assistant for State Bank of Pakistan (SBP).

STRICT RULES:

1. If question is NOT related to banking or SBP documents:
   - Say only: "This is not a banking related question. Please ask about SBP banking regulations."
   - Do NOT mention any sources
   - Do NOT provide any other information

2. If question IS banking related but answer not in context:
   - Say only: "This information is not available in the provided SBP documents."
   - Do NOT mention any sources

3. If question IS banking related AND answer IS in context:
   - Use bullet points maximum 5-6
   - Use simple and easy English
   - If difficult word used, explain in brackets
   - Always mention document name and page number at end
   - Example: (Source: SBP_AML_CFT_Regulations.pdf, Page 5)

4. For conversation memory:
   - Remember previous questions and answers
   - If asked about previous question, refer to chat history

5. NEVER make up information
6. NEVER add sources not in context
7. Be professional and precise"""

    # Start with system message
    messages = [{"role": "system", "content": system_prompt}]

    # Add chat history for memory
    for msg in chat_history:
        messages.append(msg)

    # Add current query with context
    user_prompt = f"""Context from SBP banking documents:
{context}

Question: {query}

Please provide a clear answer based on the context.
Always mention document name and page number."""

    messages.append({"role": "user", "content": user_prompt})

    # Call Groq API
    response = client.chat.completions.create(
        model=GROQ_TEXT_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.1
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "model": GROQ_TEXT_MODEL,
        "query": query
    }


def generate_answer_from_image(
    image_description: str,
    query: str,
    context: str,
    chat_history: list = []
) -> dict:
    """
    Generate answer for image based query
    Combines image description with document context
    Returns dict with answer and metadata
    """
    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """You are a helpful banking document assistant for State Bank of Pakistan (SBP).

STRICT RULES:

1. Analyze both image description and document context
2. Use bullet points maximum 5-6
3. Use simple and easy English
4. If difficult word used, explain in brackets
5. Always mention document name and page number
   Example: (Source: SBP_Document.pdf, Page 3)
6. If information not available say:
   "This information is not available in the provided SBP documents."
7. NEVER make up information
8. Be professional and precise"""

    # Start with system message
    messages = [{"role": "system", "content": system_prompt}]

    # Add chat history
    for msg in chat_history:
        messages.append(msg)

    # Combine image and context
    user_prompt = f"""Image Analysis:
{image_description}

Related Context from SBP banking documents:
{context}

Question: {query}

Please provide a clear answer based on both image and context.
Always mention document name and page number."""

    messages.append({"role": "user", "content": user_prompt})

    # Call Groq API
    response = client.chat.completions.create(
        model=GROQ_TEXT_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.1
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "model": GROQ_TEXT_MODEL,
        "query": query,
        "image_description": image_description
    }