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
from app import *
from db import *
# from pages.MODELS import MODEL


## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

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
                case st.selectbox: st.session_state.FORM_FIELDS[field.LABEL] = st.selectbox(LABEL, options=field.VALUE, index=None)
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
                    INFOBOX(f"Complete all * fields")
                    return False
        ## CHECK Id
        if st.session_state.FORM_FIELDS.get("Id"):
            if SQL_ID_COUNT(st.session_state.TABLE, st.session_state.FORM_FIELDS['Id']):
                INFOBOX(f"< {st.session_state.FORM_FIELDS['Id']} > is already in the DATABASE")
                return False
        else:
            INFOBOX(f"Id field is empty")
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
        st.session_state.FORM_BTN = None
        st.session_state.FORM_FIELDS = None
        st.rerun()

    @st.experimental_dialog("📄 NEW COMPANY")
    def COMPANIES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("FULL_NAME", "", st.text_input, True),
            FORMS.FIELD("COUNTRY", "", st.text_input, True),
            FORMS.FIELD("ADDRESS1", "", st.text_input, True),
            FORMS.FIELD("ADDRESS2", "", st.text_input, False),
            FORMS.FIELD("POST_CODE", "", st.text_input, False),
            # FORMS.FIELD("PHONE_NUMBER", "", st.text_input, False),
            FORMS.FIELD("WEB_LINK", "http://", st.text_input, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            st.session_state.FORM_FIELDS['COUNTRY'] = st.session_state.FORM_FIELDS['COUNTRY'].upper()
            if FORMS._CHECK(FIELDS):
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)

    @st.experimental_dialog("📄 NEW DEVICE TYPE")
    def DEVICE_TYPES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION", "", st.text_input, True),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            if FORMS._CHECK(FIELDS):
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)

    @st.experimental_dialog("📄 NEW MANUFACTURER")
    def MANUFACTURERS():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DIMINUTIVE", "", st.text_input, True),
            FORMS.FIELD("FULL_NAME", "", st.text_input, True),
            FORMS.FIELD("WEB_LINK", "http://", st.text_input, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            st.session_state.FORM_FIELDS['DIMINUTIVE'] = st.session_state.FORM_FIELDS['DIMINUTIVE'].upper()
            if FORMS._CHECK(FIELDS):
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)

    @st.experimental_dialog("📄 NEW MODEL")
    def MODELS():
        FIELDS = [
            FORMS.FIELD("DEVICE_TYPE", SQL_SELECT_COLUMN('DEVICE_TYPES', 'Id'), st.selectbox, True),
            FORMS.FIELD("MANUFACTURER", SQL_SELECT_COLUMN('MANUFACTURERS', 'Id'), st.selectbox, True),
            FORMS.FIELD("MODEL", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION (information described on the device)", "", st.text_input, False),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['MODEL'] = st.session_state.FORM_FIELDS['MODEL'].upper()
            DIMINUTIVE = SQL_BY_ROW("MANUFACTURERS", 'Id', st.session_state.FORM_FIELDS['MANUFACTURER'])[0]['DIMINUTIVE']
            st.session_state.FORM_FIELDS['Id'] = f"{DIMINUTIVE}_{st.session_state.FORM_FIELDS['MODEL']}".replace(chr(32), str()).upper()
            st.session_state.FORM_FIELDS['DESCRIPTION'] = st.session_state.FORM_FIELDS.pop('DESCRIPTION (information described on the device)')
            if FORMS._CHECK(FIELDS):
                VALUES = st.session_state.FORM_FIELDS
                VALUES['DB'] = DB.MODEL_DB(RANGE={}, PART_NUMBER="", SPECIFICATIONS={}).toJSON()
                FORMS._INSERT(st.session_state.TABLE, VALUES)

    @st.experimental_dialog("📄 NEW DEVICE")
    def DEVICES():
        FIELDS = [
            FORMS.FIELD("CUSTOMER", SQL_SELECT_COLUMN('COMPANIES', 'Id'), st.selectbox, False),
            FORMS.FIELD("MODEL_ID", SQL_SELECT_COLUMN('MODELS', 'Id'), st.selectbox, True),
            FORMS.FIELD("SERIAL_ID", "", st.text_input, True),
            FORMS.FIELD("INVENTORY_ID", "", st.text_input, False),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = f"{st.session_state.FORM_FIELDS['MODEL_ID']}_{st.session_state.FORM_FIELDS['SERIAL_ID']}".replace(chr(32), str()).upper()
            st.session_state.FORM_FIELDS['COMPANY_ID'] = st.session_state.FORM_FIELDS.pop('CUSTOMER')
            if FORMS._CHECK(FIELDS):
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)

    @st.experimental_dialog("📄 NEW PROCEDURE")
    def PROCEDURES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, False),
            FORMS.FIELD("DEFAULT TEST TITLE", "", st.text_input, True),
            FORMS.FIELD("INFO", "", st.text_area, True),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].replace(chr(32), str()).upper()
            # st.session_state.FORM_FIELDS
            if FORMS._CHECK(FIELDS):
                st.session_state.FORM_FIELDS['TITLE'] = st.session_state.FORM_FIELDS.pop('DEFAULT TEST TITLE')
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)

    @st.experimental_dialog("📄 NEW TEMPLATE")
    def TEMPLATES():
        FIELDS = [
            FORMS.FIELD("MODEL_ID", SQL_SELECT_COLUMN('MODELS', 'Id'), st.selectbox, True),
            FORMS.FIELD("VERSION", "", st.text_input, True),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = f"{st.session_state.FORM_FIELDS['MODEL_ID']}_{st.session_state.FORM_FIELDS['VERSION']}".replace(chr(32), str()).upper()
            if FORMS._CHECK(FIELDS):
                FORMS._INSERT(st.session_state.TABLE, st.session_state.FORM_FIELDS)


@st.cache_resource
def SQL_TABLE(TABLE: str, COUNT: int):
    print(f"SQL {TABLE} ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table(TABLE).select('*').order("Id"), ttl="10m")
    return SQL.data



## PAGE
## __________________________________________________________________________________________________

# if not st.session_state.LOGIN_STATUS:
#     st.switch_page(r"pages/LOGIN.py")

## SIDEBAR & BASIC COMPONENTS
st.logo(os.path.join(path_resources, r"LOGO2.svg"))
SIDEBAR()

st.text("✏️ SELECT TABLE")

col12, col22 = st.columns(2)

with col12:
    st.session_state.TABLE = st.selectbox("TABLES", options=[table.name for table in DB.TABLES], label_visibility='collapsed', index=None)

with col22:
    if st.button("💾 CREATE NEW ITEM", use_container_width=True):
        if not st.session_state.TABLE:
            INFOBOX("Please!! Select a valid Table")
        else:
            if st.session_state.TABLE not in dir(FORMS):
                INFOBOX("This form is not available yet")
            else:
                form = getattr(FORMS, st.session_state.TABLE)
                form()


## LOAD DATABASE
if st.session_state.TABLE and st.session_state.LOGIN_STATUS:

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

# FOOTER("FLEXICAL | DB ITEMS")