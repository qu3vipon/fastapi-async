import requests
import streamlit as st

from const import Page, SERVER_URL

st.set_page_config(page_title="Fast Async Chat", page_icon="💬")
st.title('Fast Async Chat')

if 'user_state' not in st.session_state:
    st.session_state.user_state = {"access_token": ""}

# Before login
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

    # Try login
    if submit and not st.session_state.user_state['access_token']:
        response = requests.post(
            f"{SERVER_URL}/users/login",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            access_token = response.json()["access_token"]
            st.session_state.user_state['access_token'] = access_token
            st.rerun()
        else:
            st.warning('유효하지 않은 Username 또는 Password입니다.')

# 로그인 된 경우
elif st.session_state.user_state['access_token']:
    st.success("환영합니다!")
