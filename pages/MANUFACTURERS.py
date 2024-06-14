'''
FLEXICAL DEVELOPER | MANUFACTURERS PAGE

`TASK:`
    - cachear la consulta SQL

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
from db import SQL_ID_COUNT, SQL_INSERT, SQL_MANUFACTURERS



## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None

if SSTATE.MANUFACTURERS_COUNT not in st.session_state:
    st.session_state[SSTATE.MANUFACTURERS_COUNT] = 1



## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
    st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")
    # st.sidebar.divider()
    # sd_btn_new = st.sidebar.button("💾 NEW", use_container_width=True)



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"manufacturers.svg"), use_column_width=False)
st.divider()

@st.experimental_dialog("CREATE NEW MANUFACTURER")
def FORM_NEWMANUFACTURER():

    ID = st.text_input("ID *", value="")
    DIMINUTIVE: str = st.text_input("DIMINUTIVE *", value="")
    FULL_NAME = st.text_input("FULL NAME *", value="")
    WEB_LINK = st.text_input("WEB LINK", value="")

    st.text("")
    if st.button(label="💽 CREATE NEW MANUFACTURER", use_container_width=True):
        CHECK: bool = True
        if CHECK and (not ID or not DIMINUTIVE or not FULL_NAME):
            st.warning(f"Complete all * fields", icon="⚠️")
            CHECK = False
        if CHECK and (len(DIMINUTIVE) < 2 or len(DIMINUTIVE) > 5):
            st.warning(f"< {DIMINUTIVE} > The diminutive should contain between 2 and 5 characters", icon="⚠️")
            CHECK = False
        if SQL_ID_COUNT("MANUFACTURERS", ID):
            st.warning(f"< {ID} > is already in the DATABASE", icon="🚨")
            CHECK = False
        if CHECK:
            ## INSERT
            VALUES = {
                "Id": ID.upper(), 
                "DIMINUTIVE": DIMINUTIVE.upper(),
                'FULL_NAME': FULL_NAME.upper(),
                'WEB_LINK': WEB_LINK,
                "FIRM": GET_FIRM()
            }
            SQL_INSERT("MANUFACTURERS", VALUES)
            st.session_state[SSTATE.MANUFACTURERS_COUNT] += 1
            st.info("New Manufacturer Added !!", icon='🏁')
            sleep(2)
            st.rerun()

if st.button("💾 CREATE NEW MANUFACTURER", use_container_width=True):
    FORM_NEWMANUFACTURER()



## DATABASE
## __________________________________________________________________________________________________

if st.session_state[SSTATE.DEVICETYPES_COUNT]:

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATABASE:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ DATABASE](#database)
    # """, unsafe_allow_html=True)

    placeholder = st.empty()
    if placeholder.button("🧬 LOAD DATABASE", use_container_width=True):
        with placeholder.expander("🧬 DATABASE", expanded=True):
            SQL = SQL_MANUFACTURERS(st.session_state[SSTATE.MANUFACTURERS_COUNT])
            st.dataframe(
                data=pd.DataFrame(SQL),
                use_container_width=True,
                hide_index=True
            )