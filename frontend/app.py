import streamlit as st
import requests
import uuid

# ─── CONFIG ───────────────────────────────────────────
API_BASE = "http://localhost:8000/api"
HEALTH_URL = "http://localhost:8000/health"

st.set_page_config(
    page_title="🏦 Banking Support Chatbot",
    page_icon="🏦",
    layout="centered"
)

# ─── SESSION STATE INIT ───────────────────────────────
def init_session_state():
    """Initialize all session state variables safely."""
    defaults = {
        "session_id": str(uuid.uuid4()),
        "messages": [],
        "chat_sessions": {},
        "current_chat_name": "New Chat"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ─── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.header("💬 Chats")
    
    # ─── NEW CHAT BUTTON ──────────────────────────────
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        # Save current chat before starting new one
        if st.session_state.messages:
            st.session_state.chat_sessions[st.session_state.current_chat_name] = {
                "messages": st.session_state.messages.copy(),
                "session_id": st.session_state.session_id
            }
        
        # Reset everything for fresh chat
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.current_chat_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.rerun()
    
    # ─── PREVIOUS CHATS LIST ──────────────────────────
    if st.session_state.chat_sessions:
        st.divider()
        st.caption("Previous chats")
        
        for name, session_data in list(st.session_state.chat_sessions.items()):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(f"💬 {name}", key=f"load_{name}", use_container_width=True):
                    st.session_state.messages = session_data["messages"].copy()
                    st.session_state.session_id = session_data["session_id"]
                    st.session_state.current_chat_name = name
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{name}"):
                    del st.session_state.chat_sessions[name]
                    st.rerun()
    
    st.divider()
    
    # ─── DOCUMENT UPLOAD ──────────────────────────────
    st.header("📁 Upload Documents")
    
    uploaded = st.file_uploader(
        "Upload PDF/TXT", 
        type=["pdf", "txt"],
        accept_multiple_files=False
    )
    
    if uploaded and st.button("📤 Upload", use_container_width=True):
        with st.spinner("Processing..."):
            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
            try:
                resp = requests.post(f"{API_BASE}/upload", files=files, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(f"✅ {data['message']}")
                else:
                    st.error(f"❌ {resp.text}")
            except Exception as e:
                st.error(f"❌ {e}")
    
    # ─── HEALTH STATUS ────────────────────────────────
    st.divider()
    try:
        health = requests.get(HEALTH_URL, timeout=3).json()
        if health.get("vectorstore_ready"):
            st.success("🟢 Ready")
        else:
            st.warning("🟡 No docs indexed")
    except:
        st.error("🔴 Offline")

# ─── MAIN CHAT AREA ──────────────────────────────────
st.title("🏦 Banking Support Chatbot")
st.caption("Ask about loans, credit cards, policies & FAQs")

# Show current chat name
st.caption(f"Current: {st.session_state.current_chat_name}")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 Sources"):
                for src in msg["sources"]:
                    st.markdown(f"**{src['source']}** ({src['doc_type']})")
                    st.caption(src["content"])

# ─── CHAT INPUT ──────────────────────────────────────
if prompt := st.chat_input("Ask about banking..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/chat",
                    json={"message": prompt, "session_id": st.session_state.session_id},
                    timeout=30
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data.get("answer", "")
                    sources = data.get("sources", [])
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("📄 Sources"):
                            for src in sources:
                                st.markdown(f"**{src['source']}** ({src['doc_type']})")
                                st.caption(src["content"])
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(f"Backend error: {resp.text}")
                    
            except Exception as e:
                st.error(f"❌ {e}")