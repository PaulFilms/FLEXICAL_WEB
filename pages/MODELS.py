'''
FLEXICAL DEVELOPER | MODELS

'''

## PYTHON LIBRARIES
import os, json
from time import sleep
from typing import TypedDict
from dataclasses import dataclass, asdict
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import SSTATE, USUAL_ICONS, GET_FIRM, path_resources, SIDEBAR
from db import conn, execute_query, SQL_SELECT_COLUMN, SQL_ID_COUNT, SQL_INSERT, SQL_MODELS


## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None

if SSTATE.MODELS_COUNT not in st.session_state:
    st.session_state[SSTATE.MODELS_COUNT] = 1

if 'MODEL_COUNT' not in st.session_state:
    st.session_state['MODEL_COUNT'] = 0

## OBJECTS
## __________________________________________________________________________________________________

class MODEL:

    class TypeDict(TypedDict):
        Id: str
        MODEL: str
        MANUFACTURER: str
        DEVICE_TYPE: str
        DESCRIPTION: str
        INFO: str
        DB: dict
        FIRM: str
    
    @dataclass
    class DB:
        RANGE: dict = None
        PART_NUMBER: str = ""
        SPECIFICATIONS: dict = None

        def toJSON(self) -> str:
            return json.dumps(asdict(self))



## MENU
## __________________________________________________________________________________________________

@st.experimental_dialog("NEW MODEL FORM")
def FORM_NEWMODEL():
    DEVICE_TYPE = st.selectbox("TYPE OF DEVICE *", options=SQL_SELECT_COLUMN('DEVICE_TYPES', 'Id'), index=None)
    MANUFACTURER = st.selectbox("MANUFACTURER *", options=SQL_SELECT_COLUMN('MANUFACTURERS', 'Id'), index=None)
    MODEL_ = st.text_input("MODEL *")
    DESCRIPTION = st.text_input("DESCRIPTION")
    INFO = st.text_area("INFO")

    if st.button(label="💽 CREATE NEW MODEL", use_container_width=True):
        CHECK: bool = True
        if CHECK and (not MANUFACTURER or not DEVICE_TYPE or not MODEL_):
            st.warning(f"Complete all * fields", icon=USUAL_ICONS.WARNINNG.value)
            CHECK = False
        sql = execute_query(conn.table("MANUFACTURERS").select("DIMINUTIVE").eq("Id", MANUFACTURER), ttl='10m')
        ID = f"{sql.data[0]['DIMINUTIVE']}_{MODEL_}".replace(chr(32), str())
        if SQL_ID_COUNT("MODELS", ID):
            st.warning(f"< {ID} > is already in the DATABASE", icon=USUAL_ICONS.WARNINNG.value)
            CHECK = False
        if CHECK:
            ## INSERT
            DB = MODEL.DB(RANGE={}, PART_NUMBER="", SPECIFICATIONS={})
            VALUES = {
                "Id": ID.upper(), 
                "MODEL": MODEL_.upper(),
                'MANUFACTURER': MANUFACTURER,
                'DEVICE_TYPE': DEVICE_TYPE,
                'DESCRIPTION': DESCRIPTION.upper(),
                'INFO': INFO,
                'DB': DB.toJSON(),
                "FIRM": GET_FIRM()
            }
            SQL_INSERT("MODELS", VALUES)
            st.session_state[SSTATE.MODELS_COUNT] += 1
            st.info("New Model Added !!", icon='🏁')
            sleep(3)
            st.rerun()

@st.cache_resource
def SQL_MODEL(MODEL_ID: str, COUNT: int):
    print(f"SQL MODEL DATA ({COUNT}):", GET_FIRM())
    return execute_query(conn.table('MODELS').select('*', count='exact').like("Id", MODEL_ID))


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
    st.sidebar.page_link(r"pages/MANUFACTURERS.py", label="MANUFACTURERS", icon="🚗")
    # sd_btn_new = st.sidebar.button("💾 NEW MODEL", use_container_width=True)


## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"models.svg"), use_column_width=False)
st.divider()

tab_db, tab_editor = st.tabs(["📒 DATABASE", "✏️ EDITOR"])

## DATABASE
## __________________________________________________________________________________________________

with tab_db:

    if st.button("💾 CREATE NEW MODEL", use_container_width=True): # or sd_btn_new:
        FORM_NEWMODEL()


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
                SQL = SQL_MODELS(st.session_state[SSTATE.MODELS_COUNT])
                DATAFRAME = pd.DataFrame(SQL)
                del DATAFRAME["DB"]
                st.dataframe(
                    # data=pd.DataFrame(SQL),
                    data=DATAFRAME,
                    use_container_width=True,
                    hide_index=True
                )


## EDITOR
## __________________________________________________________________________________________________

with tab_editor:

    col12, col22 = st.columns(2)

    with col12:
        MODEL_ID = st.text_input(label="✏️ ENTER MODEL Id", value="")

    with col22:

        # SQL = SQL_MODELS(st.session_state[SSTATE.MODELS_COUNT])
        # DATAFRAME = pd.DataFrame(SQL)
        # print(DATAFRAME)

        st.text("")
        with st.popover(USUAL_ICONS.EXPANDER.value):
            st.selectbox("DEVICE TYPE", options=[])
            st.selectbox("MANUFACTURER", options=[])
            st.selectbox("MODEL", options=[])

if MODEL_ID:
    SQL = SQL_MODEL(MODEL_ID, st.session_state['MODEL_COUNT'])
    print(SQL)
    # if SQL.count != 1:
    #     st.session_state[DB_DATA] = None
    #     st.session_state[MODEL_PROCEDURES] = pd.DataFrame([], columns=["PROCEDURE_ID"])
    #     st.warning(f"< {MODEL_ID} > don't exits", icon="⚠️")
    # else:
    #     CURRENT_MODEL = MODEL.TypeDict(**SQL.data[0])
    #     CURRENT_DB = CURRENT_MODEL["DB"]