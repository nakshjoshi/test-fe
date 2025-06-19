import streamlit as st
import requests
import time

# =========================
# CONFIG
# =========================
CONTROLLER_API_URL = "http://3.84.184.18:9000"  # Controller backend
GENAI_API_URL = "http://3.84.184.18:8000"       # GenAI backend container

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
        resp = requests.post(f"{CONTROLLER_API_URL}/start-container")
        st.sidebar.success(resp.json().get("status", "Started ✅"))

        # === WARM-UP POLLING ===
        def wait_until_backend_ready(timeout=20):
            start = time.time()
            while time.time() - start < timeout:
                try:
                    res = requests.get(f"{GENAI_API_URL}/")
                    if res.status_code == 200:
                        return True
                except:
                    pass
                time.sleep(4)  # retry every 4 seconds
            return False

        with st.spinner("🌀 Warming up GenAI container... Please wait."):
            if wait_until_backend_ready():
                st.sidebar.success("✅ Backend is ready!")
            else:
                st.sidebar.warning("⚠️ Backend did not become ready in time.")

    except Exception as e:
        st.sidebar.error(f"Error starting: {e}")

if col2.button("⏹️ Stop"):
    try:
        resp = requests.post(f"{CONTROLLER_API_URL}/stop-container")
        st.sidebar.success(resp.json().get("status", "Stopped ❌"))
    except Exception as e:
        st.sidebar.error(f"Error stopping: {e}")

if col3.button("🗑️ Remove"):
    try:
        resp = requests.post(f"{CONTROLLER_API_URL}/remove-container")
        st.sidebar.success(resp.json().get("status", "Removed 🧹"))
    except Exception as e:
        st.sidebar.error(f"Error removing: {e}")

# Container status
try:
    status = requests.get(f"{CONTROLLER_API_URL}/container-status").json()
    st.sidebar.markdown(f"**Status:** `{status.get('status', 'Unknown')}`")
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
                res = requests.post(f"{GENAI_API_URL}/ask", json={"query": query})
                if res.status_code == 200:
                    answer = res.json().get("answer")
                    st.success("✅ Answer:")
                    st.markdown(answer)
                else:
                    st.error("Server error. Try again.")
            except Exception as e:
                st.error(f"Request failed: {e}")