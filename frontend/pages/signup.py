import time

import streamlit as st

import requests

from const import Page, SERVER_URL

st.set_page_config(page_title="Fast Async Chat", page_icon="💬")
st.page_link(Page.HOME, label="홈으로 돌아가기", icon="🏠")

st.title("회원가입")

new_username = st.text_input("새 사용자 이름")
new_password = st.text_input("새 비밀번호", type="password")

if st.button("회원가입"):
    response = requests.post(
        f"{SERVER_URL}/users/sign-up",
        json={"username": new_username, "password": new_password}
    )

    if response.status_code == 201:
        st.success(f"{new_username}님, 회원가입이 완료되었습니다!")
        time.sleep(1)
        st.switch_page(Page.HOME)
    else:
        st.error(f"회원가입에 실패했습니다: {response.json().get('detail')}")
