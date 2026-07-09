import streamlit as st
import requests
import os


def render_chat_interface(api_url: str):
    """
    Chat interface component for banking document queries
    Supports text queries with chat memory
    Shows sources with page numbers
    Allows individual message deletion
    """
    st.subheader("Chat with Banking Documents")

    # Greetings list
    greetings = [
        "hi", "hello", "hey",
        "how are you", "help",
        "hi!", "hello!", "hey!",
        "good morning", "good evening",
        "good afternoon", "salam",
        "assalam"
    ]

    # Display messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Sources with page numbers
            if (
                message["role"] == "assistant"
                and "sources" in message
                and message["sources"]
            ):
                with st.expander("View Sources"):
                    chunks = message.get("chunks", [])
                    if chunks:
                        seen = set()
                        for chunk in chunks:
                            source = chunk["metadata"].get("source", "unknown")
                            page = chunk["metadata"].get("page", "N/A")
                            filename = os.path.basename(source)
                            key = f"{filename} - Page {page}"
                            if key not in seen:
                                st.write(f"- {key}")
                                seen.add(key)
                    else:
                        unique_sources = list(set(message["sources"]))
                        for source in unique_sources:
                            filename = os.path.basename(source)
                            st.write(f"- {filename}")

            # Delete button
            col_a, col_b = st.columns([6, 1])
            with col_b:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.messages.pop(i)
                    if len(st.session_state.chat_history) >= 2:
                        st.session_state.chat_history.pop()
                        st.session_state.chat_history.pop()
                    st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask about SBP banking regulations..."):

        is_greeting = prompt.lower().strip() in greetings

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        if is_greeting:
            greeting_response = """Hello! I am your SBP Banking Assistant.

I can help you with:
- Banking regulations and policies
- Loan and financing requirements
- General SBP banking queries

Please ask me any question about SBP banking documents!"""

            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting_response,
                "sources": [],
                "chunks": []
            })
            st.rerun()

        else:
            with st.spinner("Searching banking documents..."):
                try:
                    response = requests.post(
                        f"{api_url}/query/text",
                        json={
                            "query": prompt,
                            "chat_history": st.session_state.chat_history
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()
                        answer = data["answer"]
                        sources = data["sources"]
                        chunks = data.get("retrieved_chunks", [])

                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": prompt
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer
                        })

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                            "chunks": chunks
                        })

                        st.rerun()

                    else:
                        st.error("Error getting answer!")

                except Exception as e:
                    st.error(f"Connection error: {str(e)}")