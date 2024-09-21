import streamlit as st
from menus import *
from db import *
from time import sleep
from dataclasses import dataclass
from typing import TypeVar, Union
import pandas as pd
from flexical.database import tables, table_db, field, data_types
from flexical.report import REPORT


## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'FORM_FIELDS' not in st.session_state:
    st.session_state.FORM_FIELDS = None

if 'FORM_BTN' not in st.session_state:
    st.session_state.FORM_BTN = None


## TOOLS
## __________________________________________________________________________________________________

T = TypeVar('T', bound=Union[st.checkbox, st.text_input, st.text_area, st.selectbox])

class FORMS:
    
    @dataclass
    class FIELD():
        LABEL: str
        VALUE: bool | str | int | float | list | tuple = None
        TYPE: T = st.text_input
        MANDATORY: bool = False

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

    def _CHECK(TABLE: str, FIELDS: dict):
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
            if supabase.table(TABLE).select('*', count='exact').like('Id', st.session_state.FORM_FIELDS['Id']).execute().count:
            # if SQL_ID_COUNT(st.session_state.TABLE, st.session_state.FORM_FIELDS['Id']):
                INFOBOX(f"< {st.session_state.FORM_FIELDS['Id']} > is already in the DATABASE")
                return False
        else:
            INFOBOX(f"Id field is empty")
            return False
        ## ALL CHECKED
        return True

    def _INSERT(TABLE: str, VALUES: dict) -> None:
        sql_insert(TABLE, VALUES)
        st.info("NEW ITEM ADDED !!", icon='🏁')
        sleep(2)
        st.session_state.FORM_BTN = None
        st.session_state.FORM_FIELDS = None
        st.rerun()

    @st.dialog("📄 NEW COMPANY")
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
            if FORMS._CHECK('COMPANIES', FIELDS):
                FORMS._INSERT('COMPANIES', st.session_state.FORM_FIELDS)

    @st.dialog("📄 NEW DEVICE TYPE")
    def DEVICE_TYPES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION", "", st.text_input, True),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].upper()
            if FORMS._CHECK('DEVICE_TYPES', FIELDS):
                FORMS._INSERT('DEVICE_TYPES', st.session_state.FORM_FIELDS)

    @st.dialog("📄 NEW MANUFACTURER")
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
            if FORMS._CHECK('MANUFACTURERS', FIELDS):
                FORMS._INSERT('MANUFACTURERS', st.session_state.FORM_FIELDS)

    @st.dialog("📄 NEW MODEL")
    def MODELS():
        if 'DEVICE_TYPES' not in st.session_state:
            st.session_state.DEVICE_TYPES = 1
        if 'MANUFACTURERS' not in st.session_state:
            st.session_state.MANUFACTURERS = 1
        FIELDS = [
            FORMS.FIELD("DEVICE_TYPE", sql_column('DEVICE_TYPES', 'Id', st.session_state.DEVICE_TYPES), st.selectbox, True),
            FORMS.FIELD("MANUFACTURER", sql_column('MANUFACTURERS', 'Id',  st.session_state.MANUFACTURERS), st.selectbox, True),
            FORMS.FIELD("MODEL", "", st.text_input, True),
            FORMS.FIELD("DESCRIPTION (information described on the device)", "", st.text_input, False),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['MODEL'] = st.session_state.FORM_FIELDS['MODEL'].upper()
            DIMINUTIVE = sql_row("MANUFACTURERS", 'Id', st.session_state.FORM_FIELDS['MANUFACTURER'], st.session_state.MANUFACTURERS)['DIMINUTIVE']
            st.session_state.FORM_FIELDS['Id'] = f"{DIMINUTIVE}_{st.session_state.FORM_FIELDS['MODEL']}".replace(chr(32), str()).upper()
            st.session_state.FORM_FIELDS['DESCRIPTION'] = st.session_state.FORM_FIELDS.pop('DESCRIPTION (information described on the device)')
            if FORMS._CHECK('MODELS', FIELDS):
                VALUES = st.session_state.FORM_FIELDS
                VALUES['DB'] = {f.name: None for f in table_db.MODELS}
                FORMS._INSERT('MODELS', VALUES)

    @st.dialog("📄 NEW DEVICE")
    def DEVICES():
        if 'COMPANIES' not in st.session_state:
            st.session_state.COMPANIES = 1
        if 'MODELS' not in st.session_state:
            st.session_state.MODELS = 1
        FIELDS = [
            FORMS.FIELD("CUSTOMER", sql_column('COMPANIES', 'Id', st.session_state.COMPANIES), st.selectbox, False),
            FORMS.FIELD("MODEL_ID", sql_column('MODELS', 'Id', st.session_state.MODELS), st.selectbox, True),
            FORMS.FIELD("SERIAL_ID", "", st.text_input, True),
            FORMS.FIELD("INVENTORY_ID", "", st.text_input, False),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = f"{st.session_state.FORM_FIELDS['MODEL_ID']}_{st.session_state.FORM_FIELDS['SERIAL_ID']}".replace(chr(32), str()).upper()
            st.session_state.FORM_FIELDS['COMPANY_ID'] = st.session_state.FORM_FIELDS.pop('CUSTOMER')
            if FORMS._CHECK('DEVICES', FIELDS):
                FORMS._INSERT('DEVICES', st.session_state.FORM_FIELDS)

    @st.dialog("📄 NEW PROCEDURE")
    def PROCEDURES():
        FIELDS = [
            FORMS.FIELD("Id", "", st.text_input, True),
            FORMS.FIELD("DEFAULT TEST TITLE", "", st.text_input, True),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        # DB_DEFAULT = {f.name: None for f in table_db.PROCEDURES}
        # DB_DEFAULT[table_db.PROCEDURES.REPORT.name] = {f.name: None for f in REPORT.fields}
        # DB_DEFAULT[table_db.PROCEDURES.REPORT.name][REPORT.fields.TESTREPORT.name] = {f.name: None for f in REPORT.TESTREPORT.fields}
        # DB_DEFAULT[table_db.PROCEDURES.REPORT.name][REPORT.fields.MEASUREMENT_UNITS.name] = {f.name: None for f in REPORT.MEASUREMENT_UNITS.fields}
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = st.session_state.FORM_FIELDS['Id'].replace(chr(32), str()).upper()
            if FORMS._CHECK('PROCEDURES', FIELDS):
                st.session_state.FORM_FIELDS['TITLE'] = st.session_state.FORM_FIELDS.pop('DEFAULT TEST TITLE')
                # st.session_state.FORM_FIELDS['DB'] = DB_DEFAULT
                FORMS._INSERT('PROCEDURES', st.session_state.FORM_FIELDS)

    @st.dialog("📄 NEW TEMPLATE")
    def TEMPLATES():
        if 'MODELS' not in st.session_state:
            st.session_state.MODELS = 1
        FIELDS = [
            FORMS.FIELD("MODEL_ID", sql_column('MODELS', 'Id', st.session_state.MODELS), st.selectbox, True),
            FORMS.FIELD("VERSION", "", st.text_input, True),
            FORMS.FIELD("INFO", "", st.text_area, False),
        ]
        FORMS._GET_FIELDS(FIELDS)
        if st.session_state.FORM_BTN:
            st.session_state.FORM_FIELDS['Id'] = f"{st.session_state.FORM_FIELDS['MODEL_ID']}_{st.session_state.FORM_FIELDS['VERSION']}".replace(chr(32), str()).upper()
            if FORMS._CHECK('TEMPLATES', FIELDS):
                FORMS._INSERT('TEMPLATES', st.session_state.FORM_FIELDS)


## PAGE
## __________________________________________________________________________________________________


st.text("SELECT TABLE")

col12, col22 = st.columns(2)

with col12:
    TABLE = st.selectbox("TABLES", options=[table.name for table in TABLES], label_visibility='collapsed', index=None)

with col22:
    BTN_NEWITEM = None
    if st.session_state.role == ROLES.ADMIN:
        BTN_NEWITEM = st.button("💾 CREATE NEW ITEM", use_container_width=True)

if BTN_NEWITEM:
    # if st.button("💾 CREATE NEW ITEM", use_container_width=True):
    if not TABLE:
        INFOBOX("Please!! Select a valid Table")
    else:
        # INFOBOX("This form is not available yet")
        if TABLE not in dir(FORMS):
            INFOBOX("This form is not available yet")
        else:
            form = getattr(FORMS, TABLE)
            form()
        # FORM(TABLE)

if TABLE:
    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATA:', divider='blue')

    if TABLE not in st.session_state:
        st.session_state[TABLE] = 1

    SQL = sql_table(TABLE, st.session_state[TABLE])
    DATAFRAME = pd.DataFrame(SQL)
    if "DB" in DATAFRAME.columns:
        del DATAFRAME["DB"]
    if "PYDATA" in DATAFRAME.columns:
        del DATAFRAME["PYDATA"]

    with st.popover(":material/menu:", help="TABLE OPTIONS"):
        st.text("EXPORT TO .xlsx")
        st.text("EXPORT TO .pdf")

    st.dataframe(
        data=DATAFRAME,
        use_container_width=True,
        hide_index=True,
        column_config={colum: st.column_config.TextColumn(label=colum, width=None) for colum in list(DATAFRAME.columns)}
    )


