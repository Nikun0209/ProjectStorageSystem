import streamlit as st # type: ignore
import index
import login
import pandas as pd # type: ignore
import connect_db
import hashlib
from streamlit_option_menu import option_menu # type: ignore
from datetime import datetime

def home():
    username = index.controller.get('username')  # Lấy username từ controller

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
                        menu_title = "Setting",
                        options = ["User", "Projects"],
                        icons = ["people", "book"],
                        menu_icon = "gear",
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
                            clear_data = pd.DataFrame(user_result, columns=["ID", "User ID", "Name", "Email", "Password", "Role Login", "Status", "Modified By", "Modified_At"])
                            st.dataframe(clear_data)
                        else:
                            st.write("No users added yet.")
                            
                    elif selected == "Projects":
                        st.header("Projects Settings")
                        st.write("This is the projects settings page.")
                elif selected == "logout":
                    index.controller.remove('username')  # Xóa thông tin người dùng khỏi cookie
                    st.success("Bạn đã đăng xuất thành công!")  # Hiển thị thông báo đăng xuất
                    st.rerun()
    else:
        login.login()
