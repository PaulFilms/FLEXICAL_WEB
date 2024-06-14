'''
FLEXICAL v3 | MENU

`INFO:`

https://docs.streamlit.io/develop/tutorials/multipage/st.page_link-nav

Info about login
https://github.com/mkhorasani/Streamlit-Authenticator
pip install streamlit-authenticator

'''

## PYTHON LIBRARIES
import os
from datetime import datetime
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st

## INTERNAL
...


## COMPONENTS
## __________________________________________________________________________________________________

path_resources = r"resources"

class SSTATE(Enum):
    LOGIN_STATUS = "LOGIN_STATUS"
    DEVICETYPES_COUNT = "DEVICETYPES_COUNT"
    MANUFACTURERS_COUNT = "MANUFACTURERS_COUNT"
    MODELS_COUNT = "MODELS_COUNT"
    PROCEDURES_COUNT = "PROCEDURES_COUNT"

class USUAL_ICONS(Enum):
    HOME = "🏠"
    EXIT = "⛔"
    SAVE = "💾"
    DELETE = "🗑️"
    INSERT = "➕"
    UPDATE = "🔄"
    CHECK = "✅" # ✔️ ✅
    WARNINNG = "🚨" # 🚨 🚩 ⚠️
    UP = "🔼"
    DOWN = "🔽"
    QUESTION = "❓"
    EXPANDER = chr(8801)

def INFOBOX(info: str):
    return st.warning(info, icon="🚨")

def GET_FIRM() -> str:
    date_now = datetime.now().strftime("%Y-%m-%d / %H:%M")
    return f"{os.getlogin()} [{date_now}]"

def COL_SCI(label: str):
    return st.column_config.NumberColumn(label=label, format="%.2e")


## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None


## MENUS
## __________________________________________________________________________________________________

@st.experimental_dialog("LOGIN")
def LOGIN():
    st.session_state[SSTATE.LOGIN_STATUS] = None

    USERNAME = st.text_input("USERNAME *")
    PASSWORD = st.text_input("PASSWORD *", type='password')

    st.text("") # SEPARATOR
    if st.button(label="☝️ LOGIN", use_container_width=True):
        if USERNAME == None or USERNAME == str():
            INFOBOX("PLEASE pon el nombre bro")
            return
        # if PASSWORD == None or PASSWORD == str():
        
        # INFOBOX(PASSWORD)
        # return None
        st.session_state[SSTATE.LOGIN_STATUS] = USERNAME
        st.rerun()

def SIDEBAR():
    if st.session_state[SSTATE.LOGIN_STATUS]:
        with st.sidebar.popover(f"🌐 {st.session_state[SSTATE.LOGIN_STATUS]}", use_container_width=True):

            if st.button("⚙️ PROFILE", use_container_width=True):
                st.switch_page(r"pages/PROFILE.py")

            if st.button(f"{USUAL_ICONS.EXIT.value} [Log out]", use_container_width=True, help="Logout"):
                st.session_state[SSTATE.LOGIN_STATUS] = None
                st.switch_page(r"app.py")
                st.rerun()
            
            # st.sidebar.page_link(r"pages/PROFILE.py", label="PROFILE", icon="⚙️")
        
        # st.sidebar.divider()
        # st.sidebar.page_link("app.py", label="HOME", icon="🏠")
        # st.sidebar.page_link(r"pages/DEVICE_TYPE.py", label="DEVICE TYPES", icon="🚗")
        # st.sidebar.page_link(r"pages/MANUFACTURERS.py", label="MANUFACTURERS", icon="🚗")
        # st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")
        # st.sidebar.page_link(r"pages/DEVICES.py", label="DEVICES", icon="📻")
        # st.sidebar.divider()
        # st.sidebar.page_link(r"pages/COMPANIES.py", label="COMPANIES", icon="🧬")
        # st.sidebar.page_link(r"pages/TEMPLATES.py", label="TEMPLATES", icon="📱")

        # st.sidebar.divider()
        # st.sidebar.page_link(r"pages/TEST.py", label="TEST", icon="🧬")

        # st.toast("Estas dentro Bro !!")

    else: 
        if st.sidebar.button("🙋‍♀️🙋‍♂️ LOGIN", use_container_width=True):
            LOGIN()
