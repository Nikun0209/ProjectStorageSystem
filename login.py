import streamlit as st # type: ignore
import index
import home
import connect_db

def login():
    col1, col2, col3 = st.columns([3, 2, 3])

    with col2:
        # Nếu chưa đăng nhập, hiển thị form đăng nhập
        st.subheader("🤖 Sign In to BenCodeX")
        
        # Nhập tên người dùng và mật khẩu
        username_input = st.text_input("Email")
        password_input = st.text_input("Password", type='password')
        
        if st.button("Login"):
            # # Kiểm tra tên người dùng và mật khẩu
            # connect_db.create_user_table()
            # result = connect_db.login_user(username_input, password_input)

            # if result or (username_input == "administrator" and password_input == "123"):  # Thay thế bằng điều kiện kiểm tra thực tế
            if username_input == "administrator" and password_input == "123":  # Thay thế bằng điều kiện kiểm tra thực tế
                index.controller.set('username', username_input)
                home.home()
                st.rerun()
            else:
                st.warning("Tên người dùng hoặc mật khẩu không đúng.")