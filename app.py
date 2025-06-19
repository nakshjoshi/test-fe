import streamlit as st
import requests
import time

# =========================
# CONFIG
# =========================
API_BASE_URL = "http://3.84.184.18:8000/"  # Replace with actual public IP or domain

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="GovScheme AI", page_icon="📜", layout="centered")
st.title("🧠 Government Schemes RAG Assistant")
st.markdown("Ask anything about Indian government schemes or manage backend containers.")

# =========================
# CONTAINER MANAGEMENT
# =========================

st.sidebar.subheader("🛠️ Backend Container Control")

col1, col2, col3 = st.sidebar.columns(3)

if col1.button("▶️ Start"):
    try:
        resp = requests.post(f"{API_BASE_URL}/start-container")
        st.sidebar.success("Container started ✅")
    except Exception as e:
        st.sidebar.error(f"Error starting: {e}")

if col2.button("⏹️ Stop"):
    try:
        resp = requests.post(f"{API_BASE_URL}/stop-container")
        st.sidebar.success("Container stopped ❌")
    except Exception as e:
        st.sidebar.error(f"Error stopping: {e}")

if col3.button("🗑️ Remove"):
    try:
        resp = requests.post(f"{API_BASE_URL}/remove-container")
        st.sidebar.success("Container removed 🧹")
    except Exception as e:
        st.sidebar.error(f"Error removing: {e}")

# Container status
try:
    status = requests.get(f"{API_BASE_URL}/container-status").json()
    st.sidebar.markdown(f"**Status:** `{status.get('status')}`")
except:
    st.sidebar.warning("⚠️ Could not fetch container status.")

# =========================
# CHATBOT INTERFACE
# =========================

st.subheader("💬 Ask a Question")
query = st.text_input("Enter your question below:")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{API_BASE_URL}/ask", json={"query": query})
                if res.status_code == 200:
                    answer = res.json().get("answer")
                    st.success("✅ Answer:")
                    st.markdown(answer)
                else:
                    st.error("Server error. Try again.")
            except Exception as e:
                st.error(f"Request failed: {e}")
