'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import SSTATE, GET_FIRM, path_resources, SIDEBAR
from db import conn, execute_query

## MENU
## __________________________________________________________________________________________________

class TABLES(Enum):
    COMPANIES = "COMPANIES"
    DEVICE_TYPES = "DEVICE TYPES"
    MANUFACTURERS = "MANUFACTURERS"
    MODELS = "MODELS"
    DEVICES = "DEVICES"
    PROCEDURES = "PROCEDURES"
    TEMPLATES = "TEMPLATES"

class FORMS:
    @st.experimental_dialog("NEW MODEL FORM")
    def MODELS():
        st.write('MODELS')
    

@st.cache_resource
def SQL_TABLE(TABLE: str, COUNT: int):
    print(f"SQL {TABLE} ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table(TABLE).select('*').order("Id"), ttl="10m")
    return SQL.data


## SESSION STATES
## __________________________________________________________________________________________________

if not st.session_state[SSTATE.LOGIN_STATUS]:
    st.switch_page(r"pages/PROFILE.py")

if 'COUNT' not in st.session_state:
    st.session_state.COUNT = 1


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")


## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.divider()

col12, col22 = st.columns(2)

with col12:
    TABLE = st.selectbox("TABLES", options=[table.value for table in TABLES], label_visibility='collapsed', index=None)

with col22:
    if st.button("CREATE NEW", use_container_width=True):
        form = getattr(FORMS, TABLE)
        form()


if TABLE and st.session_state[SSTATE.LOGIN_STATUS]:

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATABASE:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ DATABASE](#database)
    # """, unsafe_allow_html=True)

    table = [tbl.name for tbl in TABLES if tbl.value == TABLE][0]
    if table not in st.session_state:
        st.session_state[table] = 1
    SQL = SQL_TABLE(table, st.session_state[table])
    DATAFRAME = pd.DataFrame(SQL)
    if "DB" in DATAFRAME.columns:
        del DATAFRAME["DB"]
    if "PYDATA" in DATAFRAME.columns:
        del DATAFRAME["PYDATA"]
    st.dataframe(
        data=DATAFRAME,
        use_container_width=True,
        hide_index=True
    )