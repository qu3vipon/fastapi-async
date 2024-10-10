import streamlit as st
import websocket

from _const import Page, SERVER_URL, WEBSOCKET_URL

st.set_page_config(page_title="Fast Async Chat", page_icon="💬")
st.page_link(Page.HOME, label="홈으로 돌아가기", icon="🏠")

friend_username = st.session_state.chat_state["friend_username"]
st.title(f"{friend_username} 님과의 채팅")

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 나의 메시지는 오른쪽에 표시하도록 정렬
st.markdown(
    """
<style>
    .st-emotion-cache-4oy321 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 웹 소켓 연결
try:
    ws = websocket.create_connection(f"{WEBSOCKET_URL}/ws")
    while True:
        # 이전 대화 내역 조회
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="assets/friend.png"):
                st.markdown(message["content"])

        # 메시지 전송
        if prompt := st.chat_input("메세지를 입력하세요.."):
            with st.chat_message("ai", avatar="assets/me.png"):
                st.markdown(prompt)

            st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

        result = ws.recv()
        st.write(result)
except Exception as e:
    st.error("Failed to establish a WebSocket connection: " + str(e))
