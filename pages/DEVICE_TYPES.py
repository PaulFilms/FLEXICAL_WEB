'''
FLEXICAL DEVELOPER | MANUFACTURERS PAGE

`TASK:`
    - ...

`WARNINGS:`
    - ...

'''

## PYTHON LIBRARIES
import os
from time import sleep

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import SSTATE, GET_FIRM, path_resources, SIDEBAR
from db import SQL_ID_COUNT, SQL_INSERT, SQL_DEVICE_TYPES



## SESSION STATES
## __________________________________________________________________________________________________

if not st.session_state[SSTATE.DEVICETYPES_COUNT]:
    st.switch_page(r"pages/PROFILE.py")

if SSTATE.DEVICETYPES_COUNT not in st.session_state:
    st.session_state[SSTATE.DEVICETYPES_COUNT] = 1



## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/MANUFACTURERS.py", label="MANUFACTURERS", icon="🚗")
    st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")

# if st.session_state[SSTATE.DEVICETYPES_COUNT]:
#     st.sidebar.divider()
#     sd_btn_new = st.sidebar.button("💾 NEW", use_container_width=True)



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"devicetypes.svg"), use_column_width=False)
st.divider()

@st.experimental_dialog("CREATE NEW DEVICE")
def FORM_NEW_DEVICETYPE():
    
    ID = st.text_input("ID *", value="")
    DESCRIPTION = st.text_input("DESCRIPTION *", value="")

    st.text("")
    if st.button(label="💽 CREATE NEW DEVICE TYPE", use_container_width=True):
        CHECK: bool = True
        if CHECK and (not ID or not DESCRIPTION):
            st.warning(f"Complete all * fields", icon="⚠️")
            CHECK = False
        if SQL_ID_COUNT("DEVICE_TYPES", ID):
            st.warning(f"< {ID} > is already in the DATABASE", icon="🚨")
            CHECK = False
        if CHECK:
            ## INSERT
            VALUES = {
                "Id": ID.upper(), 
                "DESCRIPTION": DESCRIPTION,
                "FIRM": GET_FIRM()
            }
            SQL_INSERT("DEVICE_TYPES", VALUES)
            st.session_state[SSTATE.DEVICETYPES_COUNT] += 1
            st.info("New Device Type Added !!", icon='🏁')
            sleep(3)
            st.rerun()

if st.session_state[SSTATE.LOGIN_STATUS]:
    if st.button("💾 CREATE NEW DEVICE TYPE", use_container_width=True):
        FORM_NEW_DEVICETYPE()



## DATABASE
## __________________________________________________________________________________________________

if st.session_state[SSTATE.LOGIN_STATUS]:

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATABASE:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ DATABASE](#database)
    # """, unsafe_allow_html=True)

    placeholder = st.empty()
    if placeholder.button("🧬 LOAD DATABASE", use_container_width=True):
        with placeholder.expander("🧬 DATABASE", expanded=True):
            SQL = SQL_DEVICE_TYPES(st.session_state[SSTATE.DEVICETYPES_COUNT])
            st.dataframe(
                data=pd.DataFrame(SQL),
                use_container_width=True,
                hide_index=True
            )