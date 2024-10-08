import streamlit as st # type: ignore
import connect_db
import time
import pandas as pd # type: ignore
import hashlib

from streamlit_cookies_controller import CookieController # type: ignore
from streamlit_option_menu import option_menu # type: ignore
from datetime import datetime

st.set_page_config(
    page_title="BenCodeX",
    page_icon="🤖",
    layout="wide"
)

# Khởi tạo CookieController
controller = CookieController()

def login():
    col1, col2, col3 = st.columns([3, 2, 3])

    with col2:
        # Nếu chưa đăng nhập, hiển thị form đăng nhập
        st.subheader("🤖 Sign In to BenCodeX")
        
        # Nhập tên người dùng và mật khẩu
        username_input = st.text_input("Email or User ID")
        password_input = st.text_input("Password", type='password')
        
        if st.button("Login"):
            # Kiểm tra tên người dùng và mật khẩu
            result = connect_db.login_user(username_input, password_input)

            if result or (username_input == "admin" and password_input == "123"):  # Thay thế bằng điều kiện kiểm tra thực tế
                controller.set('username', username_input)
                placeholder = st.empty()

                placeholder.progress(0, "Wait for it...")
                time.sleep(1)
                placeholder.progress(50, "Wait for it...")
                time.sleep(1)
                placeholder.progress(100, "Wait for it...")
                time.sleep(1)

                st.rerun()
                home()

            else:
                st.warning("Login failed. Please check your username and password.")

def home():
    username = controller.get('username')  # Lấy username từ controller

    if username:
        user_name = connect_db.get_user_name(username, username)

        if user_name:
            user_name= user_name["name"]
        else:
            user_name = "Admin"

        container = st.container(border=True)
        col1, col2, col3 = st.columns([1,8,1])
        
        with container:
            with col2:
                with st.sidebar:
                    selected = option_menu(
                        menu_title = "Menu",
                        options = ["home", "contact", "setting", "logout"],
                        icons = ["house", "envelope", "gear", "arrow-right"],
                        menu_icon = "cast",
                        default_index = 0, 
                        styles = {
                            "icon" : {
                                "color" : "yellow", 
                                "font-size": "22px"
                            },
                            "nav-link" : {
                                "font-size" : "20px",
                                "text-align" : "left",
                                "margin" : "0px",
                                "--hover-color" : "#eee",
                                "text-transform" : "capitalize"
                            }
                        }
                    )

                # Hiển thị tiêu đề theo lựa chọn
                if selected == "home":
                    st.title(f"Hello, {user_name}!")
                elif selected == "contact":
                    st.title(f"You have selected {selected}")
                elif selected == "setting":
                    selected = option_menu(
                        menu_title = "",
                        options = ["User", "Projects"],
                        icons = ["people", "book"],
                        default_index = 0,
                        orientation = "horizontal",
                        styles = {
                            "icon" : {
                                "color" : "yellow", 
                                "font-size": "22px"
                            },
                            "nav-link" : {
                                "font-size" : "20px",
                                "text-align" : "center",
                                "margin" : "0px",
                                "--hover-color" : "#eee",
                                "text-transform" : "capitalize"
                            }
                        }
                    )

                    if selected == "User":
                        st.header("👤 User Management")

                        # Dữ liệu người dùng mẫu (nếu không có dữ liệu nào)
                        if "data" not in st.session_state:
                            st.session_state.data = {}

                        @st.dialog("👤 Add User")
                        # Hàm để hiển thị dialog thêm người dùng
                        def add_user_dialog():
                            user_id = st.text_input("User ID")
                            name = st.text_input("Name")
                            email = st.text_input("Email")
                            password = st.text_input("Password")
                            status = st.text_input("Status")

                            if st.button("💾 Save"):
                                if name and email and password and status:
                                    if name not in st.session_state.data:
                                        # Lấy ngày giờ hiện tại
                                        current_datetime = datetime.now()

                                        # Định dạng ngày giờ
                                        modified_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                        id = hashlib.md5(modified_at.encode()).hexdigest()

                                        # Thêm thông tin người dùng
                                        connect_db.create_user_table()
                                        connect_db.add_user(id, user_id, name, email, password, 1, 1, username, modified_at)

                                        st.success(f"User `{name}` added successfully!")
                                        st.rerun()  # Tải lại ứng dụng để cập nhật
                                    else:
                                        st.error(f"User with name `{name}` already exists.")
                                else:
                                    st.error("Please fill in all fields.")

                        if st.button("➕ Add User", use_container_width=True):
                            add_user_dialog()
                        

                        # Hiển thị bảng dữ liệu người dùng
                        user_result = connect_db.view_all_users()

                        if user_result:
                           # Tạo DataFrame từ kết quả
                            clear_data = pd.DataFrame(user_result, columns=["ID", "User ID", "Name", "Email", "Password", "Role", "Status", "Modified By", "Modified At"])

                            # Thêm CSS để làm cho nút có độ rộng 100%
                            st.markdown(
                                """
                                <style>
                                    .full-width-delete-button {
                                        width: 100%;
                                        display: block;
                                        border: none;
                                    }

                                    .full-width-delete-button:hover {
                                        background-color: red;
                                        color: white;
                                    }

                                    .full-width-edit-button {
                                        width: 100%;
                                        display: block;
                                        border: none;
                                    }

                                    .full-width-edit-button:hover {
                                        background-color: green;
                                        color: white;
                                    }

                                    .full-width-public-button {
                                        width: 100%;
                                        display: block;
                                        border: none;
                                        background-color: green;
                                        color: white;
                                    }

                                    .full-width-public-button:hover {
                                        background-color: green;
                                        color: black;
                                    }

                                    
                                    .full-width-private-button {
                                        width: 100%;
                                        display: block;
                                        border: none;
                                        background-color: red;
                                        color: white;
                                    }

                                    .full-width-private-button:hover {
                                        background-color: red;
                                        color: black;
                                    }

                                </style>
                                """, 
                                unsafe_allow_html=True
                            )

                            for index, row in clear_data.iterrows():
                                data = row  # Truy cập vào Series của hàng
                                
                                # HTML cho từng thẻ người dùng
                                table_user = f"""
                                <div class="card" style="margin-bottom: 10px; padding: 10px; border: 1px solid #ccc;">
                                    <div class="card-header">
                                        <h5 class="card-title">User ID: {data["ID"]}</h5>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-text">Name: {data["Name"]}</p>
                                        <p class="card-text">Email: {data["Email"]}</p>
                                        <p class="card-text">Modified by: {data["Modified By"]} - {data["Modified At"]}</p>
                                    </div>
                                </div>
                                """

                                # Hiển thị thẻ người dùng
                                st.markdown(table_user, unsafe_allow_html=True)

                                # Tạo hai nút trong cùng một hàng với độ rộng 100%
                                col1, col2, col3 = st.columns(3)
                               
                                with col1:
                                    st.markdown(f'''
                                            <button class="full-width-delete-button" onclick="window.location.href=\'#\'">➖ Delete</button>
                                        ''', unsafe_allow_html=True)

                                with col2:
                                    st.markdown(f'''
                                        <button class="full-width-edit-button" onclick="window.location.href=\'#\'">✏️ Edit</button>
                                    ''', unsafe_allow_html=True)

                                with col3:
                                    # Tạo nút Public hoặc Private dựa trên trạng thái
                                    if data["Status"] == 1:
                                        st.markdown(f'''
                                            <button class="full-width-public-button" onclick="window.location.href=\'#\'">
                                                🌍 Public
                                            </button>
                                        ''', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'''
                                            <button class="full-width-private-button" onclick="window.location.href=\'#\'">
                                                🔒 Private
                                            </button>
                                        ''', unsafe_allow_html=True)


                        else:
                            st.write("No users added yet.")
                            
                    elif selected == "Projects":
                        st.header("Projects Settings")
                        st.write("This is the projects settings page.")
                elif selected == "logout":
                    controller.remove('username')  # Xóa thông tin người dùng khỏi cookie
                    st.success("You have successfully logged out!")  # Hiển thị thông báo đăng xuất
                    st.rerun()
    else:
        login()


# Kiểm tra xem người dùng đã đăng nhập chưa
def main():
    username = controller.get('username')  # Lấy username từ cookie

    if username:
        home()  # Nếu đã đăng nhập, gọi hàm home
    else:
        login()

if __name__ == "__main__":  # Kiểm tra xem tệp đang được chạy chính hay không
    main()  # Gọi hàm main

