import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components
from ui.components.chat_interface import render_chat_interface
from ui.components.image_uploader import render_image_uploader
from ui.components.file_uploader import render_file_uploader

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Page configuration
st.set_page_config(
    page_title="SBP Banking RAG System",
    page_icon="🏦",
    layout="wide"
)

# Main title
st.title("🏦 SBP Multimodal Banking RAG System")
st.markdown("*Ask questions about SBP banking regulations and documents*")
st.markdown("---")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.header("Document Management")

    # File uploader component
    render_file_uploader(API_URL)

    st.markdown("---")

    # Clear all chat
    if st.button("Clear All Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ─── Main Layout ─────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface component
    render_chat_interface(API_URL)

with col2:
    st.subheader("Image Query")
    st.markdown("*Upload a banking chart or document image*")

    # Image uploader component
    render_image_uploader(API_URL)