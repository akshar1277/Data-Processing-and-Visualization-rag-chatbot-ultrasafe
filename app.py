import streamlit as st
import requests
import time

# Base URL of your FastAPI backend
BASE_URL = "http://localhost:8000"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "sessions" not in st.session_state:
    st.session_state["sessions"] = []
if "current_session" not in st.session_state:
    st.session_state["current_session"] = "New Chat"
if "show_auth" not in st.session_state:
    st.session_state["show_auth"] = True
if "show_upload_modal" not in st.session_state:
    st.session_state["show_upload_modal"] = False
if "clear_signup_form" not in st.session_state:
    st.session_state["clear_signup_form"] = False
if "signup_success" not in st.session_state:
    st.session_state["signup_success"] = False

# --- Authentication Functions ---
def signup(email, password, confirm_password):
    if not email or not password or not confirm_password:
        st.error("Please fill in all fields.")
        return False

    if len(password) < 6:
        st.error("Password must be at least 6 characters.")
        return False

    if password != confirm_password:
        st.error("Passwords do not match.")
        return False
    
    response = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password, "confirm_password": confirm_password})
    print(response.status_code, response.json())
    if response.status_code in [200, 201]:
        print("Signup successful")
        return True
    else:
        st.error(response.json().get("detail", "Signup failed."))
        return False

def login(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        st.session_state["session_id"] = response.cookies.get("session_id")
        st.session_state["show_auth"] = False
        st.success("Login successful!")
        return True
    else:
        st.error(response.json().get("detail", "Login failed."))
        return False

# --- Upload Function ---
def upload_document(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    cookies = {"session_id": st.session_state["session_id"]}
    response = requests.post(f"{BASE_URL}/upload", files=files, cookies=cookies)
    if response.status_code == 200:
        return True, "Document uploaded and processed successfully!"
    else:
        return False, response.json().get("detail", "Upload failed.")

# --- Query Function ---
def send_query(query):
    cookies = {"session_id": st.session_state["session_id"]}
    response = requests.post(f"{BASE_URL}/query", json={"query": query}, cookies=cookies)
    if response.status_code == 200:
        return response.json().get("answer", "No answer found.")
    else:
        return f"Error: {response.json().get('detail', 'Query failed.')}"

# --- Authentication Modal ---
def show_auth_modal():
    with st.container():
        st.markdown("### Welcome to Document Chat Assistant")
        
        # Show signup success message
        if st.session_state.get("signup_success", False):
            st.success("Signup successful! Please log in using the Login tab.")
            st.session_state["signup_success"] = False  # Clear the message after showing
        
        tab1, tab2 = st.tabs(["Login", "Signup"])

        with tab1:
            st.markdown("#### Login to your account")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            col1, _ = st.columns([1, 3])
            with col1:
                if st.button("Login", key="login_btn"):
                    if email and password:
                        if login(email, password):
                            st.rerun()
                    else:
                        st.error("Please fill in all fields")

        with tab2:
            st.markdown("#### Create a new account")
            
            # Use empty values when form should be cleared
            if st.session_state.get("clear_signup_form", False):
                email_val = ""
                password_val = ""
                confirm_password_val = ""
            else:
                email_val = None  # Let Streamlit handle the default
                password_val = None
                confirm_password_val = None
            
            email = st.text_input("Email", key="signup_email", value=email_val)
            password = st.text_input("Password", type="password", key="signup_password", value=password_val)
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password", value=confirm_password_val)
            
            col1, _ = st.columns([1, 3])
            with col1:
                if st.button("Signup", key="signup_btn"):
                    if email and password and confirm_password:
                        if signup(email, password, confirm_password):
                            # Set flags for success message and form clearing
                            st.session_state["signup_success"] = True
                            st.session_state["clear_signup_form"] = True
                            st.rerun()
                    else:
                        st.error("Please fill in all fields")

# --- Page Config and Styling ---
st.set_page_config(page_title="Document Chat Assistant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.chat-container {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    height: 500px;
    overflow-y: auto;
}
.user-message {
    background-color: #007bff;
    color: white;
    padding: 10px 15px;
    border-radius: 18px;
    margin: 5px 0;
    max-width: 70%;
    margin-left: auto;
    text-align: right;
}
.ai-message {
    background-color: #e9ecef;
    color: #333;
    padding: 10px 15px;
    border-radius: 18px;
    margin: 5px 0;
    max-width: 70%;
    margin-right: auto;
}
.session-item {
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
    cursor: pointer;
    border: 1px solid #ddd;
}
.session-item:hover {
    background-color: #f8f9fa;
}
.upload-success {
    background-color: #d4edda;
    color: #155724;
    padding: 8px;
    border-radius: 5px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# Reset the clear form flag after it's been used
if st.session_state.get("clear_signup_form", False):
    st.session_state["clear_signup_form"] = False
    # Clear the actual session state values
    if "signup_email" in st.session_state:
        del st.session_state["signup_email"]
    if "signup_password" in st.session_state:
        del st.session_state["signup_password"]
    if "signup_confirm_password" in st.session_state:
        del st.session_state["signup_confirm_password"]

# --- AUTH CHECK ---
if st.session_state["show_auth"] or not st.session_state["session_id"]:
    show_auth_modal()
    st.stop()  # prevent rest of app from loading

# --- Main Chat Interface ---
col1, col2 = st.columns([1, 3])

# --- Sidebar: Chat Sessions ---
with col1:
    st.markdown("### 💬 Chat Sessions")

    if st.button("➕ New Chat", key="new_chat", use_container_width=True):
        st.session_state["messages"] = []
        st.session_state["current_session"] = f"Chat {len(st.session_state['sessions']) + 1}"

    st.markdown("---")
    st.markdown("#### Recent Sessions")

    if st.session_state["messages"] and st.session_state["current_session"] not in [s["name"] for s in st.session_state["sessions"]]:
        st.session_state["sessions"].append({
            "name": st.session_state["current_session"],
            "messages": st.session_state["messages"].copy(),
            "timestamp": time.time()
        })

    for i, session in enumerate(st.session_state["sessions"]):
        if st.button(f"💬 {session['name']}", key=f"session_{i}", use_container_width=True):
            st.session_state["messages"] = session["messages"].copy()
            st.session_state["current_session"] = session["name"]

    if not st.session_state["sessions"]:
        st.markdown("*No previous sessions*")

    st.markdown("---")
    if st.button("🚪 Logout", key="logout"):
        try:
            # Hit the logout API
            cookies = {"session_id": st.session_state["session_id"]}
            response = requests.post(f"{BASE_URL}/auth/logout", cookies=cookies)
            if response.status_code == 200:
                st.success("Logged out successfully.")
            else:
                st.warning("Failed to notify backend. Logging out anyway.")
        except Exception as e:
            st.warning(f"Logout request failed: {e}")

        # Clear session state regardless
        st.session_state["session_id"] = None
        st.session_state["show_auth"] = True
        st.session_state["messages"] = []
        st.session_state["sessions"] = []
        st.rerun()

# --- Main Chat Panel ---
with col2:
    st.markdown(f"### {st.session_state['current_session']}")

    chat_container = st.container()
    with chat_container:
        chat_html = '<div class="chat-container">'
        if not st.session_state["messages"]:
            chat_html += "<div class='ai-message'>🤖 Hello! I'm here to help you with your documents. You can upload a document and ask questions about it.</div>"
        else:
            for message in st.session_state["messages"]:
                if message["role"] == "user":
                    chat_html += f'<div class="user-message">{message["content"]}</div>'
                elif message["role"] in ["assistant", "system"]:
                    chat_html += f'<div class="ai-message">🤖 {message["content"]}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("---")
    with st.form(key="chat_form", clear_on_submit=True):
        chat_cols = st.columns([11, 1])
        user_input = chat_cols[0].text_input("_", key="chat_input", placeholder="Ask me anything about your documents...", label_visibility="hidden")
        upload_icon_clicked = chat_cols[1].form_submit_button("📎", use_container_width=True)
        send_button = st.form_submit_button("📤 Send", use_container_width=True)

        if upload_icon_clicked:
            st.session_state["show_upload_modal"] = True

        if send_button and user_input:
            st.session_state["messages"].append({
                "role": "user",
                "content": user_input
            })
            with st.spinner("Getting response..."):
                ai_response = send_query(user_input)
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": ai_response
                })
            st.rerun()

    # Upload Modal
    if st.session_state["show_upload_modal"]:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "doc", "docx", "txt"], key="modal_file_upload")
        colu1, colu2 = st.columns([1, 1])
        upload_btn = colu1.button("Upload", key="modal_upload_btn")
        cancel_btn = colu2.button("Cancel", key="modal_cancel_btn")
        if upload_btn and uploaded_file:
            with st.spinner("Uploading document..."):
                success, message = upload_document(uploaded_file)
                if success:
                    st.session_state["messages"].append({
                        "role": "system",
                        "content": f"✅ Document '{uploaded_file.name}' uploaded successfully!"
                    })
                else:
                    st.session_state["messages"].append({
                        "role": "system",
                        "content": f"❌ {message}"
                    })
            st.session_state["show_upload_modal"] = False
            st.rerun()
        if cancel_btn:
            st.session_state["show_upload_modal"] = False
            st.rerun()