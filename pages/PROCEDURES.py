'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import SSTATE, GET_FIRM, path_resources, SIDEBAR
from db import SQL_PROCEDURES



## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None

if SSTATE.PROCEDURES_COUNT not in st.session_state:
    st.session_state[SSTATE.PROCEDURES_COUNT] = 1

## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
    st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"procedures.svg"), use_column_width=False)
st.divider()

tab_db, tab_editor = st.tabs(["📒 DATABASE", "✏️ EDITOR"])

## DATABASE
## __________________________________________________________________________________________________

with tab_db:

    if st.button("💾 CREATE NEW PROCEDURE", use_container_width=True): # or sd_btn_new:
        # FORM_NEWMODEL()
        pass


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
                SQL = SQL_PROCEDURES(st.session_state[SSTATE.PROCEDURES_COUNT])
                DATAFRAME = pd.DataFrame(SQL)
                del DATAFRAME["DB"]
                del DATAFRAME["PYDATA"]
                st.dataframe(
                    # data=pd.DataFrame(SQL),
                    data=DATAFRAME,
                    use_container_width=True,
                    hide_index=True
                )


## EDITOR
## __________________________________________________________________________________________________
