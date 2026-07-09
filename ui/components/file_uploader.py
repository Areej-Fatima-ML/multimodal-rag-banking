import streamlit as st
import requests


def render_file_uploader(api_url: str):
    """
    File upload component for banking documents
    Supports PDF, DOCX, PPTX formats
    """
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx", "pptx"],
        help="Upload banking documents"
    )

    if uploaded_file:
        if st.button("Upload Document", use_container_width=True):
            with st.spinner("Uploading..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{api_url}/upload",
                        files=files
                    )
                    if response.status_code == 200:
                        st.success(f"{uploaded_file.name} uploaded!")
                    else:
                        st.error("Upload failed!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")