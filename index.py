import streamlit as st # type: ignore
import home
import login
from streamlit_cookies_controller import CookieController # type: ignore

st.set_page_config(
    page_title="BenCodeX",
    page_icon="🤖",
    layout="wide"
)

# Khởi tạo CookieController
controller = CookieController()

# Kiểm tra xem người dùng đã đăng nhập chưa
def main():
    username = controller.get('username')  # Lấy username từ cookie

    if username:
        home.home()  # Nếu đã đăng nhập, gọi hàm home
    else:
        login.login()  # Nếu chưa đăng nhập, gọi hàm login

if __name__ == "__main__":  # Kiểm tra xem tệp đang được chạy chính hay không
    main()  # Gọi hàm main

