import os
import requests
import streamlit as st

# ================================
# CONFIG & STATE
# ================================
st.set_page_config(
    page_title="Zentro – Intelligent Content Management",
    page_icon="🧠",
    layout="wide",
)

# ================================
# CUSTOM CSS & THEME
# ================================
st.markdown("""
<style>
    /* GLOBAL THEME */
    :root {
        --primary: #6C5CE7;
        --secondary: #A29BFE;
        --bg-dark: #0F0F13;
        --bg-card: #1E1E24;
        --text-main: #FFFFFF;
        --text-sub: #B2BEC3;
        --accent: #00CEC9;
    }

    /* BACKGROUND */
    .stApp {
        background-color: var(--bg-dark);
        background-image: radial-gradient(circle at 50% 0%, #2D3436 0%, #0F0F13 70%);
    }

    /* HEADERS */
    h1, h2, h3 {
        color: var(--text-main) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* CARDS / CONTAINERS */
    .css-1r6slb0, .css-12oz5g7, .stExpander {
        background-color: var(--bg-card);
        border-radius: 12px;
        border: 1px solid #2D3436;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
    }
    
    /* INPUTS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #2D3436;
        color: white;
        border-radius: 8px;
        border: 1px solid #636E72;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }

    /* CHAT BUBBLES */
    .stChatMessage {
        background-color: transparent;
        border: none;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(108, 92, 231, 0.1);
        border-left: 3px solid var(--primary);
        border-radius: 0 12px 12px 0;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(45, 52, 54, 0.3);
        border-right: 3px solid var(--secondary);
        border-radius: 12px 0 0 12px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #151518;
        border-right: 1px solid #2D3436;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_doc_id" not in st.session_state:
    st.session_state.current_doc_id = None

# ================================
# SIDEBAR
# ================================
with st.sidebar:
    st.title("🧠 Zentro")
    if st.button("🔄 Refresh Page"):
        st.rerun()
    
    st.header("⚙️ Settings")
    default_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    backend_url = st.text_input("Backend URL", value=default_url)
    st.session_state.backend_url = backend_url

    if st.button("Check Connection"):
        try:
            r = requests.get(f"{backend_url}/health", timeout=2)
            if r.status_code == 200:
                st.success("Connected!")
            else:
                st.error(f"Status: {r.status_code}")
        except Exception as e:
            st.error(f"Failed: {e}")

    st.markdown("---")
    st.header("📚 Knowledge Base")
    
    # Refresh button for docs
    if st.button("Refresh List"):
        st.rerun()

    # Fetch docs
    try:
        r = requests.get(f"{backend_url}/rag/list", timeout=2)
        if r.status_code == 200:
            docs = r.json().get("documents", [])
            
            # File Selection
            doc_options = {"All Documents": None}
            for d in docs:
                doc_options[d["filename"]] = d["doc_id"]
            
            selected_name = st.selectbox("Select Document", list(doc_options.keys()))
            st.session_state.current_doc_id = doc_options[selected_name]

            # Clear Button
            if st.button("Clear Knowledge Base", type="primary"):
                try:
                    r_clear = requests.post(f"{backend_url}/rag/clear", timeout=5)
                    if r_clear.status_code == 200:
                        st.success("Knowledge Base Cleared!")
                        st.session_state.current_doc_id = None
                        st.rerun()
                    else:
                        st.error("Failed to clear KB.")
                except Exception as e:
                    st.error(f"Error: {e}")

        else:
            st.warning("Could not fetch document list.")
    except:
        st.warning("Backend offline or unreachable.")
    
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #636E72; font-size: 0.8rem; margin-top: 2rem;">
            Developed with ❤️ by <b>Alan Cyril Sunny</b>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================================
# MAIN UI
# ================================
# Hero Section
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem; background: linear-gradient(135deg, rgba(108, 92, 231, 0.2) 0%, rgba(162, 155, 254, 0.1) 100%); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #FFFFFF 0%, #A29BFE 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🧠 Zentro 2.0</h1>
    <p style="font-size: 1.2rem; color: #B2BEC3;">Local-First Intelligent Content Platform</p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
        <span style="padding: 0.4rem 1rem; background: rgba(108, 92, 231, 0.2); border-radius: 20px; color: #A29BFE; font-size: 0.9rem;">✨ Vision</span>
        <span style="padding: 0.4rem 1rem; background: rgba(0, 206, 201, 0.2); border-radius: 20px; color: #00CEC9; font-size: 0.9rem;">📄 Docs</span>
        <span style="padding: 0.4rem 1rem; background: rgba(253, 121, 168, 0.2); border-radius: 20px; color: #FD79A8; font-size: 0.9rem;">💬 Chat</span>
    </div>
</div>
""", unsafe_allow_html=True)

tab_vision, tab_docs, tab_chat = st.tabs(
    ["🖼️ Vision", "📄 Documents", "💬 Chat"]
)

# ================================
# VISION TAB
# ================================
with tab_vision:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        with st.container(border=True):
            st.subheader("📤 Upload Image")
            img_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
            img_instruction = st.text_area("Instruction", value="Describe this image in detail.", height=100)
            analyze_btn = st.button("✨ Analyze Image", type="primary", use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("👁️ Preview")
            if img_file:
                st.image(img_file, caption="Uploaded Image", use_container_width=True)
            else:
                st.info("Upload an image to see preview.")
    
    if analyze_btn and img_file:
        st.markdown("---")
        with st.container(border=True):
            st.subheader("📝 Analysis Result")
            try:
                files = {"file": (img_file.name, img_file.getvalue(), img_file.type)}
                data = {"instruction": img_instruction}
                with st.spinner("Analyzing..."):
                    r = requests.post(f"{backend_url}/analyze/image", files=files, data=data, timeout=120)
                    try:
                        resp = r.json()
                    except ValueError:
                        st.error(f"Backend returned non-JSON response: {r.text[:200]}")
                        resp = {"error": "Invalid response from backend"}
                
                if "error" in resp:
                    st.error(resp["error"])
                else:
                    st.markdown("### Result")
                    st.markdown(resp["result"])
            except Exception as e:
                st.error(f"Error: {e}")

# ================================
# DOCS TAB
# ================================
with tab_docs:
    with st.container(border=True):
        st.subheader("📄 Document Summarization")
        
        doc_file = st.file_uploader("Upload Document (PDF/TXT)", type=["pdf", "txt"])
        doc_instruction = st.text_area("Instruction", value="Summarize this document and extract key points, entities, and dates.", height=100, key="doc_instr")
        
        if st.button("⚡ Analyze Document", type="primary", use_container_width=True):
            if doc_file:
                try:
                    files = {"file": (doc_file.name, doc_file.getvalue(), doc_file.type)}
                    data = {"instruction": doc_instruction}
                    with st.spinner("Analyzing..."):
                        r = requests.post(f"{backend_url}/analyze/document", files=files, data=data, timeout=240)
                        try:
                            resp = r.json()
                        except ValueError:
                            st.error(f"Backend returned non-JSON response: {r.text[:200]}")
                            resp = {"error": "Invalid response from backend"}
                    
                    if "error" in resp:
                        st.error(resp["error"])
                    else:
                        st.markdown("### Result")
                        st.markdown(resp["result"])
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please upload a document.")

# ================================
# CHAT TAB
# ================================
with tab_chat:
    st.subheader("💬 Chat with your Knowledge Base")
    
    # Upload Section in Expander to save space
    with st.expander("📤 Upload New Document to Knowledge Base"):
        rag_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"], key="rag_upload")
        if st.button("Index Document"):
            if rag_file:
                try:
                    files = {"file": (rag_file.name, rag_file.getvalue(), rag_file.type)}
                    with st.spinner("Indexing..."):
                        r = requests.post(f"{backend_url}/rag/upload", files=files, timeout=240)
                        resp = r.json()
                    
                    if "error" in resp:
                        st.error(resp["error"])
                    else:
                        st.success(f"Indexed {rag_file.name} successfully!")
                        st.rerun() # Refresh list
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Select a file first.")

    st.markdown("---")

    # Chat Interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get Answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Prepare history for backend (exclude current prompt as it's sent in 'question')
                    # Actually backend expects 'chat_history' + 'question'.
                    # We send previous messages as history.
                    history = [
                        {"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages[:-1]
                    ]
                    
                    payload = {
                        "question": prompt,
                        "chat_history": history,
                        "doc_id": st.session_state.get("current_doc_id")
                    }
                    
                    r = requests.post(f"{backend_url}/rag/ask", json=payload, timeout=120)
                    try:
                        resp = r.json()
                    except ValueError:
                        answer = f"Error: Backend returned non-JSON response: {r.text[:200]}"
                        resp = {"error": "Invalid response"}
                    
                    if "error" in resp:
                        answer = f"Error: {resp['error']}"
                    else:
                        answer = resp["answer"]
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"Connection Error: {e}")
