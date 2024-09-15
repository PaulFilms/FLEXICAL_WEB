import os
import streamlit as st
from menus import *

if 'role' not in st.session_state.role:
    st.session_state.role = None

col13, col23, col33 = st.columns([1,1,1])

with col23:
    st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer
    st.session_state.role = None
    USERNAME = st.text_input("USER NAME OR MAIL *")
    PASSWORD = st.text_input("PASSWORD *", type='password')
    st.text("") # SEPARATOR
    BTN = st.button(label="🪪 LOG IN", use_container_width=True)
    st.page_link(page=r"navigation/home.py", label="Forgot your password?")

    if BTN:
        if not USERNAME or USERNAME == str():
            INFOBOX("PLEASE pon el nombre bro")
        # else:
        #     if "@" in USERNAME:
        #         SQL = SQL_BY_ROW("USERS", "MAIL", USERNAME)
        #     else:
        #         SQL = SQL_BY_ROW("USERS", "Id", USERNAME.upper())
        #     if len(SQL) == 1:
        #         USER = SQL[0]["Id"]
        #         st.session_state.LOGIN_STATUS = USER
        #     else:
        #         INFOBOX("INVALID USER/MAIL")
        
        ## PASSWORD CHECK
        # if PASSWORD == None or PASSWORD == str():
            # INFOBOX(PASSWORD)

        ## LOGIN
        # if st.session_state.LOGIN_STATUS:
        #     sleep(3)
        #     st.switch_page(r"pages/HOME.py")