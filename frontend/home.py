import requests
import streamlit as st

from _const import Page, SERVER_URL

st.set_page_config(page_title="Fast Async Chat", page_icon="💬")
st.title('Fast Async Chat')

# State 초기화
if 'user_state' not in st.session_state:
    st.session_state.user_state = {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJpc2EiOjE3Mjg1MjU1MTAuMDAyNzI4NX0.0myC5SdAUG7lZw57Hvj4vv2wVHw17DHdf3b-TcLTaB4"}
if "chat_state" not in st.session_state:
    st.session_state.chat_state = {"chat_room_id": 0, "friend_id": 0, "friend_username": "Unknown"}

#######################################################################

# 로그인 화면
if not st.session_state.user_state["access_token"]:
    username = st.text_input('사용자 이름')
    password = st.text_input('비밀번호', type='password')
    submit = st.button('로그인')

    st.divider()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.write("아직 회원이 아닌가요?")
    with col2:
        if st.button("회원가입 하기"):
            st.switch_page(Page.SIGNUP)

    #######################################################################

    # 로그인 시도
    if submit and not st.session_state.user_state['access_token']:
        response = requests.post(
            f"{SERVER_URL}/users/login",
            json={"username": username, "password": password}
        )

        if response.ok:
            access_token = response.json()["access_token"]
            st.session_state.user_state['access_token'] = access_token
            st.rerun()
        else:
            st.warning('유효하지 않은 Username 또는 Password입니다.')

#######################################################################

# 로그인 이후
elif access_token := st.session_state.user_state['access_token']:
    st.success("환영합니다!")

    # 채팅 룸 조회
    response = requests.get(f"{SERVER_URL}/chat-rooms", headers={"Authorization": f"Bearer {access_token}"})
    chat_rooms = response.json()["chat_rooms"]

    friend_ids_in_chat = {r["friend_id"] for r in chat_rooms}

    # 사용자 조회
    response = requests.get(f"{SERVER_URL}/users", headers={"Authorization": f"Bearer {access_token}"})
    users = response.json()["users"]

    #######################################################################

    st.divider()
    st.header("👥 사용자 목록")
    st.write("")

    for user in users:
        # 채팅방이 생성되지 않은 사용자만
        if user["id"] in friend_ids_in_chat:
            continue

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(user["username"])

        with col2:
            if st.button(f"친구 추가", key=user["id"]):
                # 채팅방 생성 요청
                requests.post(f"{SERVER_URL}/chat-rooms", headers={"Authorization": f"Bearer {access_token}"},
                                         json={"friend_id": user["id"]})
                st.rerun()

    #######################################################################

    st.divider()
    st.header("💬 채팅 목록")
    st.write("")

    for room in chat_rooms:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(room["friend_username"])

        with col2:
            if st.button(f"채팅하기", key=room["id"]):
                st.session_state.chat_state["chat_room_id"] = room["id"]
                st.session_state.chat_state["friend_username"] = room["friend_username"]
                st.session_state.chat_state["friend_id"] = room["friend_id"]
                st.switch_page(Page.CHAT)
