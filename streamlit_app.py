import streamlit as st
import requests
import uuid
import time

# Cấu hình trang
st.set_page_config(
    page_title="Chatbot tư vấn quy chế học vụ HUIT",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS với animations (giữ nguyên màu gốc Streamlit)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Montserrat:wght@400;500;600;700&display=swap');

/* Áp dụng font Roboto cho toàn bộ trang và tất cả components */
html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif !important;
}

.stApp, .stApp * {
    font-family: 'Roboto', sans-serif !important;
}

/* Chat messages */
.stChatMessage, .stChatMessage * {
    font-family: 'Roboto', sans-serif !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Roboto', sans-serif !important;
}

/* Input fields */
.stTextInput input, .stChatInput textarea, .stChatInput input {
    font-family: 'Roboto', sans-serif !important;
}

/* Sidebar */
section[data-testid="stSidebar"], section[data-testid="stSidebar"] * {
    font-family: 'Roboto', sans-serif !important;
}

/* Headers và text */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    font-family: 'Roboto', sans-serif !important;
}

/* Markdown content */
.stMarkdown, .stMarkdown * {
    font-family: 'Roboto', sans-serif !important;
}

/* stDecoration gradient trắng xám sang đen */
[data-testid="stDecoration"] {
    background: linear-gradient(90deg, #ffffff, #a0a0a0, #404040, #000000) !important;
}

/* Fade-in animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Pulse animation for robot icon */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

/* Float animation */
@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-5px);
    }
}

/* Bounce animation */
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}

/* Slide in from left */
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Slide in from right */
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Custom title with animation */
.animated-title {
    animation: fadeInUp 0.8s ease-out;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    font-family: 'Montserrat', sans-serif !important;
    margin-top: -55px !important;
}

.logo-container {
    display: inline-block;
    margin-bottom: 10px;
}

.animated-logo {
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
}

.animated-logo:hover {
    animation: pulse 0.5s ease-in-out;
}

/* Caption animation */
.animated-caption {
    animation: fadeIn 1s ease-out 0.3s both;
    font-size: 1rem !important;
    font-family: 'Montserrat', sans-serif !important;
     margin-top: -15px !important;
}

/* Sidebar animation */
section[data-testid="stSidebar"] {
    animation: slideInLeft 0.5s ease-out;
}

/* Button hover animation */
.stButton > button {
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Chat message animations */
.stChatMessage {
    animation: fadeInUp 0.4s ease-out;
}

/* Chat avatar icons - đổi thành màu trắng */
.stChatMessage [data-testid="chatAvatarIcon-user"],
.stChatMessage [data-testid="chatAvatarIcon-assistant"] {
    background-color: transparent !important;
    color: white !important;
}

.stChatMessage [data-testid="chatAvatarIcon-user"] svg,
.stChatMessage [data-testid="chatAvatarIcon-assistant"] svg {
    fill: white !important;
    color: white !important;
}

/* Fallback cho các version Streamlit khác */
.stChatMessage .stAvatar {
    background-color: transparent !important;
}

.stChatMessage .stAvatar svg {
    fill: white !important;
    color: white !important;
}

/* Info box animation */
.stAlert {
    animation: fadeIn 0.5s ease-out;
}

/* Footer styling */
.footer-text {
    text-align: center;
    font-size: 0.875rem;
    animation: fadeIn 1s ease-out;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px;
    background: linear-gradient(to top, rgba(14, 17, 23, 0.95), transparent);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
}

/* Tech badge styling */
.tech-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin: 2px;
    opacity: 0;
    animation: fadeInUp 0.5s ease-out forwards;
}

.tech-badge:nth-child(1) { animation-delay: 0.1s; }
.tech-badge:nth-child(2) { animation-delay: 0.2s; }
.tech-badge:nth-child(3) { animation-delay: 0.3s; }
</style>
""", unsafe_allow_html=True)

# Header với animation - Logo (CSS căn giữa)
st.markdown("""
<style>
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    padding-left: 140px;
}
</style>
""", unsafe_allow_html=True)
st.image("logo.png", width=400)

st.markdown("""
<div style="text-align: center; padding: 0.5rem 0;">
    <div class="animated-title">TRA CỨU QUY CHẾ HỌC VỤ</div>
</div>
<p class="animated-caption" style="text-align: center;">
    ARC hỗ trợ bạn tra cứu quy chế học vụ, quy định của Khoa Công nghệ thông tin
</p>
""", unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Cài đặt")
    
    # Hiển thị session ID
    st.info(f"**Session ID:**\n\n`{st.session_state.session_id[:16]}...`")
    
    # Nút tạo chat mới
    if st.button("Chat Mới", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Thông tin
    st.subheader(" Hướng dẫn")
    st.write("- Đặt câu hỏi về học vụ, quy chế, thông tin trường")
    st.write("- Nhấn 'Chat Mới' để bắt đầu cuộc trò chuyện mới")
    
    st.divider()
    
    st.subheader("Công nghệ")
    st.write("**RAG**: Hybrid Search (Vector + Keyword)")
    st.write("**LLM**: Qwen3 4B (Ollama)")
    st.write("**Memory**: ConversationSummaryBufferMemory")
    st.write("**Vector DB**: Supabase")

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Thêm câu hỏi của user vào messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Hiển thị câu hỏi của user
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gọi API và streaming response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Gọi API backend
            response = requests.post(
                "http://localhost:8000/ask",
                json={
                    "question": prompt,
                    "session_id": st.session_state.session_id
                },
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                # Stream response
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            else:
                full_response = f" Lỗi: {response.status_code}"
                message_placeholder.markdown(full_response)
        
        except requests.exceptions.ConnectionError:
            full_response = "Không thể kết nối đến server. Hãy đảm bảo server đang chạy tại `http://localhost:8000`"
            message_placeholder.markdown(full_response)
        except requests.exceptions.Timeout:
            full_response = "Timeout: Server mất quá nhiều thời gian để trả lời."
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Lỗi: {str(e)}"
            message_placeholder.markdown(full_response)
    
    # Lưu response vào session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer với animation
st.markdown("""
<div class="footer-text">
    <span style="animation: pulse 2s infinite;"></span> 
    ARC Chatbot © 2025 | Powered by Phuoc & Hoang
</div>
""", unsafe_allow_html=True)

