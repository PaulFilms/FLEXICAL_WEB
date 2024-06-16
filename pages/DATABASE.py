'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from time import sleep
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import USUAL_ICONS, SSTATE, GET_FIRM, path_resources, SIDEBAR, SB_EDITORS
from db import conn, execute_query, SQL_ID_COUNT, SQL_INSERT

## MENU
## __________________________________________________________________________________________________

class TABLES(Enum):
    DEVICE_TYPES = "DEVICE TYPES"
    MANUFACTURERS = "MANUFACTURERS"
    MODELS = "MODELS"
    COMPANIES = "COMPANIES"
    DEVICES = "DEVICES"
    PROCEDURES = "PROCEDURES"
    TEMPLATES = "TEMPLATES"

class FORMS:
    class FIELDS(Enum):
        TEXT = st.text
        INFO = st.text_area
        SELECT = st.selectbox

    def INSERT(TABLE: str, VALUES: dict) -> None:
        SQL_INSERT(TABLE, VALUES)
        if TABLE not in st.session_state:
            st.session_state[TABLE] = 1
        st.session_state[TABLE] += 1
        st.info("NEW ITEM ADDED !!", icon='🏁')
        sleep(4)
        st.rerun()

    @st.experimental_dialog("NEW DEVICE TYPE")
    def DEVICE_TYPES():
        ## FIELDS
        ID = st.text_input("ID *", value="")
        DESCRIPTION = st.text_input("DESCRIPTION *", value="")
        ## 
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
                # SQL_INSERT("DEVICE_TYPES", VALUES)
                # st.session_state[SSTATE.DEVICETYPES_COUNT] += 1
                # st.info("New Device Type Added !!", icon='🏁')
                # sleep(3)
                # st.rerun()
                FORMS.INSERT(TABLES.DEVICE_TYPES.name, VALUES)
    
    @st.experimental_dialog("NEW MODEL FORM")
    def MODELS():
        st.write('MODELS')

    @st.experimental_dialog("NEW PROCEDURE FORM")
    def PROCEDURES():
        ID = st.text_input("Id *")
        TITLE = st.text_input("DEFALUT TEST TITLE *")
        INFO = st.text_area("INFO")

        if st.button(label="💽 CREATE NEW PROCEDURE", use_container_width=True):
            CHECK: bool = True
            if CHECK and (not ID or not TITLE or not INFO):
                st.warning(f"Complete all * fields", icon=USUAL_ICONS.WARNINNG.value)
                CHECK = False
            if SQL_ID_COUNT("PROCEDURES", ID):
                st.warning(f"< {ID} > is already in the DATABASE", icon="🚨")
                CHECK = False
            if CHECK:
                ## INSERT
                VALUES = {
                    "Id": ID.upper(), 
                    "TITLE": TITLE.upper(),
                    "INFO": INFO,
                    "FIRM": GET_FIRM()
                }
                SQL_INSERT("PROCEDURES", VALUES)
                st.session_state[SSTATE.PROCEDURES_COUNT] += 1
                st.info("New Procedure Added !!", icon='🏁')
                sleep(3)
                st.rerun()
    

@st.cache_resource
def SQL_TABLE(TABLE: str, COUNT: int):
    print(f"SQL {TABLE} ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table(TABLE).select('*').order("Id"), ttl="10m")
    return SQL.data


## SESSION STATES
## __________________________________________________________________________________________________

if not st.session_state[SSTATE.LOGIN_STATUS]:
    st.switch_page(r"pages/PROFILE.py")

# if 'COUNT' not in st.session_state:
#     st.session_state.COUNT = 1


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    # st.sidebar.page_link(r"pages/DATABASE.py", label="DATABASE", use_container_width=True) # , icon="🧬" / ":blue-background[DATABASE]"
    SB_EDITORS()


## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
# st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer

st.text("✏️ SELECT TABLE")

col12, col22 = st.columns(2)

with col12:
    TABLE = st.selectbox("TABLES", options=[table.value for table in TABLES], label_visibility='collapsed', index=None)

with col22:
    if st.button("💾 CREATE NEW ITEM", use_container_width=True):
        if not TABLE:
            st.warning("Please!! Select a valid Table", icon=USUAL_ICONS.WARNINNG.value)
        else:
            form = getattr(FORMS, [tbl.name for tbl in TABLES if tbl.value == TABLE][0])
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
        hide_index=True,
        column_config={colum: st.column_config.TextColumn(label=colum, width=None) for colum in list(DATAFRAME.columns)}
    )

    with st.popover(USUAL_ICONS.EXPANDER.value, help="TABLE OPTIONS"):
        st.text("EXPORT TO .xlsx")
        st.text("EXPORT TO .pdf")

## ____________________________________________________________________________________________________________________________

# st.write(dir(FORMS))