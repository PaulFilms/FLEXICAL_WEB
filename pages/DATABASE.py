'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from time import sleep
from enum import Enum, auto
from dataclasses import dataclass
from typing import TypeVar, Union, TypedDict

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import USUAL_ICONS, SSTATE, GET_FIRM, path_resources, SIDEBAR, SB_EDITORS
from db import DB, conn, execute_query, SQL_ID_COUNT, SQL_INSERT


## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state.FORM_FIELDS = None

if not st.session_state[SSTATE.LOGIN_STATUS]:
    st.switch_page(r"pages/PROFILE.py")

if "TABLE" not in st.session_state: 
    st.session_state.TABLE = None

if 'FORM_FIELDS' not in st.session_state:
    st.session_state.FORM_FIELDS = None

if 'FORM_BTN' not in st.session_state:
    st.session_state.FORM_BTN = None



## MENU
## __________________________________________________________________________________________________

T = TypeVar('T', bound=Union[st.checkbox, st.text_input, st.text_area, st.selectbox])

class FORMS:
    # class FIELDS(Enum):
    #     TEXT = st.text
    #     INFO = st.text_area
    #     SELECT = st.selectbox
    
    @dataclass
    class FIELD():
        LABEL: str
        VALUE: bool | str | int | float | list | tuple = None
        TYPE: T = st.text_input
        MANDATORY: bool = False

    # @st.experimental_dialog("ADD NEW ITEM")
    def _GET_FIELDS(FIELDS: list[FIELD]):
        st.session_state.FORM_FIELDS = dict()
        for field in FIELDS:
            LABEL = field.LABEL
            if field.MANDATORY:
                LABEL += " *"
            match field.TYPE:
                case st.checkbox: st.session_state.FORM_FIELDS[field.LABEL] = st.checkbox(LABEL, value=field.VALUE)
                case st.text_input: st.session_state.FORM_FIELDS[field.LABEL] = st.text_input(LABEL, value=field.VALUE)
                case st.text_area: st.session_state.FORM_FIELDS[field.LABEL] = st.text_area(LABEL, value=field.VALUE)
                case st.selectbox: st.session_state.FORM_FIELDS[field.LABEL] = st.selectbox(LABEL, options=field.VALUE)
        st.text("")
        st.session_state.FORM_BTN = st.button(label="💽 CREATE NEW ITEM", use_container_width=True)

    def _CHECK(FIELDS: dict):
        ERROR: int = None
        ## MANDATORIES
        for field in FIELDS:
            if field.MANDATORY:
                if st.session_state.FORM_FIELDS[field.LABEL] == None:
                    ERROR = 1
                if st.session_state.FORM_FIELDS[field.LABEL] == str():
                    ERROR = 1
                if st.session_state.FORM_FIELDS[field.LABEL] == 0:
                    ERROR = 1
                if st.session_state.FORM_FIELDS[field.LABEL] == 0.0:
                    ERROR = 1
                if ERROR == 1:
                    st.warning(f"Complete all * fields", icon="⚠️")
                    return False
        ## CHECK Id
        if st.session_state.FORM_FIELDS.get("Id"):
            if SQL_ID_COUNT(st.session_state.TABLE, st.session_state.FORM_FIELDS['Id']):
                st.warning(f"< {st.session_state.FORM_FIELDS['Id']} > is already in the DATABASE", icon="🚨")
                return False
        else:
            st.warning(f"Id field is empty", icon="⚠️")
            return False
        ## ALL CHECKED
        return True

    def _INSERT(TABLE: str, VALUES: dict) -> None:
        VALUES["FIRM"] = GET_FIRM()
        SQL_INSERT(TABLE, VALUES)
        if TABLE not in st.session_state:
            st.session_state[TABLE] = 1
        st.session_state[TABLE] += 1
        st.info("NEW ITEM ADDED !!", icon='🏁')
        sleep(2)
        st.rerun()

    @st.experimental_dialog("NEW DEVICE TYPE")
    def DEVICE_TYPES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION", "", st.text_input, True),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            if FORMS._CHECK(FIELDS):
                VALUES = st.session_state.FORM_FIELDS
                FORMS._INSERT(st.session_state.TABLE, VALUES)

    @st.experimental_dialog("NEW MANUFACTURER")
    def MANUFACTURERS():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DIMINUTIVE", "", st.text_input, True),
            FORMS.FIELD("FULL_NAME", "", st.text_input, True),
            FORMS.FIELD("WEB_LINK", "", st.text_input, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            st.session_state.FORM_FIELDS['DIMINUTIVE'] = st.session_state.FORM_FIELDS['DIMINUTIVE'].upper()
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            if FORMS._CHECK(FIELDS):
                VALUES = st.session_state.FORM_FIELDS
                FORMS._INSERT(st.session_state.TABLE, VALUES)

    @st.experimental_dialog("NEW MODEL")
    def MODELS():
        st.write('MODELS')
        FIELDS = [
            # FORMS.FIELD("ID", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION", "", st.text_input, True),
            # DEVICE_TYPE = st.selectbox("TYPE OF DEVICE *", options=SQL_SELECT_COLUMN('DEVICE_TYPES', 'Id'), index=None)
            # MANUFACTURER = st.selectbox("MANUFACTURER *", options=SQL_SELECT_COLUMN('MANUFACTURERS', 'Id'), index=None)
            # MODEL_ = st.text_input("MODEL *")
            # DESCRIPTION = st.text_input("DESCRIPTION")
            # INFO = st.text_area("INFO")
        ]

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





## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    SB_EDITORS()


## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
# st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer

st.text("✏️ SELECT TABLE")

col12, col22 = st.columns(2)

with col12:
    st.session_state.TABLE = st.selectbox("TABLES", options=[table.name for table in DB.TABLES], label_visibility='collapsed', index=None)

with col22:
    if st.button("💾 CREATE NEW ITEM", use_container_width=True):
        if not st.session_state.TABLE:
            st.warning("Please!! Select a valid Table", icon=USUAL_ICONS.WARNINNG.value)
        else:
            form = getattr(FORMS, st.session_state.TABLE)
            form()


## LOAD DATABASE
if st.session_state.TABLE and st.session_state[SSTATE.LOGIN_STATUS]:

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATABASE:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ DATABASE](#database)
    # """, unsafe_allow_html=True)

    if st.session_state.TABLE not in st.session_state:
        st.session_state[st.session_state.TABLE] = 1
    SQL = SQL_TABLE(st.session_state.TABLE, st.session_state[st.session_state.TABLE])
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