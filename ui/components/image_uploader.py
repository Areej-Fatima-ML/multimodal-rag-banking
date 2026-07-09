import streamlit as st
import requests
import os
import io
from PIL import Image


def render_image_uploader(api_url: str):
    """
    Image upload component
    Upload once, ask multiple questions
    Results appear in chat history
    """
    st.subheader("Image Query")
    st.markdown("*Upload once, ask multiple questions*")

    # Image upload
    image_file = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    # Save image to session state
    if image_file:
        st.session_state.uploaded_image = image_file.read()
        st.session_state.uploaded_image_name = image_file.name

    # Show uploaded image preview
    if "uploaded_image" in st.session_state and st.session_state.uploaded_image:
        image = Image.open(io.BytesIO(st.session_state.uploaded_image))
        st.image(
            image,
            caption=st.session_state.get("uploaded_image_name", "Uploaded Image"),
            use_container_width=True
        )

        # Clear image button
        if st.button("Clear Image", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.uploaded_image_name = None
            st.rerun()

    # Question input
    image_question = st.text_input(
        "Ask about the image...",
        placeholder="What does this chart show?"
    )

    # Analyze button
    if st.button("Analyze Image", use_container_width=True):
        if "uploaded_image" in st.session_state and st.session_state.uploaded_image and image_question:
            with st.spinner("Analyzing image with LLaVA..."):
                try:
                    response = requests.post(
                        f"{api_url}/query/image",
                        params={"query": image_question},
                        files={
                            "file": (
                                st.session_state.uploaded_image_name,
                                io.BytesIO(st.session_state.uploaded_image),
                                "image/jpeg"
                            )
                        }
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"**[Image: {st.session_state.uploaded_image_name}]** {image_question}"
                        })
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": data["sources"],
                            "chunks": data.get("retrieved_chunks", [])
                        })

                        # Update chat history for memory
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": f"Image query: {image_question}"
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": data["answer"]
                        })

                        st.rerun()

                    else:
                        st.error("Error analyzing image!")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        elif not st.session_state.get("uploaded_image"):
            st.warning("Please upload an image first!")
        elif not image_question:
            st.warning("Please enter a question!")