'''
FLEXICAL v3 | LOGIN

Ejemplo1:
    - https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

'''

## PYTHON LIBRARIES

## IMPORTED LIBRARIES
import streamlit as st

st.set_page_config(
    page_title="FLEXICAL DEVELOPER",
    page_icon=":guardsman:",
    layout="wide", # "centered",
    initial_sidebar_state= "auto" # "collapsed"
)

## INTERNAL
from app import *
from db import *


## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None


## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))

col13, col23, col33 = st.columns([1,1,1])

with col23:
    st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer
    st.session_state.LOGIN_STATUS = None
    USERNAME = st.text_input("USER NAME OR MAIL *")
    PASSWORD = st.text_input("PASSWORD *", type='password')
    st.text("") # SEPARATOR
    BTN = st.button(label="🪪 LOG IN", use_container_width=True)
    st.page_link(page=r"pages/HOME.py", label="Forgot your password?")

    if BTN:
        if not USERNAME or USERNAME == str():
            INFOBOX("PLEASE pon el nombre bro")
        else:
            if "@" in USERNAME:
                SQL = SQL_BY_ROW("USERS", "MAIL", USERNAME)
            else:
                SQL = SQL_BY_ROW("USERS", "Id", USERNAME.upper())
            if len(SQL) == 1:
                USER = SQL[0]["Id"]
                st.session_state.LOGIN_STATUS = USER
            else:
                INFOBOX("INVALID USER/MAIL")
        
        ## PASSWORD CHECK
        # if PASSWORD == None or PASSWORD == str():
            # INFOBOX(PASSWORD)

        ## LOGIN
        if st.session_state.LOGIN_STATUS:
            sleep(3)
            st.switch_page(r"pages/HOME.py")