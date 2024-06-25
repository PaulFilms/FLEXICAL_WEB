'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from typing import Dict
from dataclasses import asdict
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from app import *
from db import *



## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

if 'TEMPLATES' not in st.session_state:
    st.session_state.TEMPLATES = 1

class TEMPLATE:

    class TypeDict(TypedDict):
        Id: str
        MODEL_ID: str
        VARSION: str
        INFO: str
        DB: dict
        PYDATA: str

    @dataclass
    class DB:
        TEST_LIST: dict = None
        def toDict(self) -> Dict[str, any]:
            return asdict(self)
    
    @dataclass
    class TEST:
        TEST: str
        PARAMETERS: str = None
        CONFIG: str = None
        INFO: str = None
        PROCEDURE_ID: str = None
        CALIBRATION: dict = None
        def toDict(self) -> Dict[str, any]:
            return asdict(self)

    class MEASURE(Enum):
        RANGE = 0
        VALUE1 = auto()
        VALUE2 = auto()
        # MEASURE = auto()
        # DEVIATION = auto()
        # SPECIFICATION = auto() # LIMIT OF ERROR
        # UNCERTAINTY = auto()
        # RESULT = auto()
        # CMC = auto()
        # ACQUISITIONS = auto() # Podria estar dentro de VALIDATION
        # VALIDATION = auto() # K_FACTOR, PROCEDURE, STANDARDS

## MENU
## __________________________________________________________________________________________________

def TEST_EDITOR(ID: str, DB: dict) -> None:
    procedures = SQL_SELECT_COLUMN("PROCEDURES", "Id")

    @st.experimental_dialog(title='✏️ EDITOR', width='small')
    def FORM_NEW():
        
        PROCEDURE_ID = st.selectbox("PROCEDURE Id *", options=procedures, index=None)
        title = str()
        if PROCEDURE_ID:
            title = SQL_BY_ROW("PROCEDURES", "Id", PROCEDURE_ID)[0]['TITLE']
        TEST = st.text_input("TEST TITLE *", value=title)
        PARAMETERS = st.text_input("TEST PARAMETERS")
        CONFIG = st.text_input("CONFIG & CONNECTIONS")
        INFO = st.text_area("INFO")
        if st.button("➕ INSERT NEW TEST", key='btn_test_ADD'):
            NEW_TEST = TEMPLATE.TEST(TEST, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, CALIBRATION={})
            DB["TEST_LIST"].append(NEW_TEST.toDict())
            try:
                SQL_UPDATE_DB("TEMPLATES", ID, DB)
                st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    @st.experimental_dialog(title='✏️ EDITOR', width='small')
    def FORM_EDIT(TEST: TEMPLATE.TEST, loc):
        indx = None
        if TEST.PROCEDURE_ID in procedures:
            indx = procedures.index(TEST.PROCEDURE_ID)
        PROCEDURE_ID = st.selectbox("PROCEDURE Id", options=procedures, index=indx)
        TITLE = st.text_input("TEST TITLE *", value=TEST.TEST)
        PARAMETERS = st.text_input("TEST PARAMETERS", value=TEST.PARAMETERS)
        CONFIG = st.text_input("CONFIG & CONNECTIONS", value=TEST.CONFIG)
        INFO = st.text_area("INFO", value=TEST.INFO)
        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_test_update'):
            EDIT_TEST = TEMPLATE.TEST(TITLE, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, TEST.CALIBRATION)
            DB["TEST_LIST"][loc] = EDIT_TEST.toDict()
            try:
                SQL_UPDATE_DB("TEMPLATES", ID, DB)
                st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    ## TABLE TEST
    DATAFRAME = pd.DataFrame(DB['TEST_LIST'], columns=['TEST', 'PARAMETERS', 'CONFIG', 'INFO', 'PROCEDURE_ID'])

    TBL_TEST = st.dataframe(
        data=DATAFRAME, 
        hide_index=True,
        on_select="rerun", # Con esta opcion aparece el selector de fila
        selection_mode=['single-row'], # "multi-column" "multi-row"
        use_container_width=True,
    )

    col13, col23, col33 = st.columns(3)

    with col13:
        if st.button(label='➕ ADD TEST', use_container_width=True):
            FORM_NEW()

    if len(TBL_TEST.selection.rows) == 1:
        loc = TBL_TEST.selection.rows[0]
        test = TEMPLATE.TEST(**dict(DATAFRAME.loc[loc]))

        print("LOAD TBL")
        print(test)

        with col23:
            if st.button(label='✏️ EDIT TEST', use_container_width=True):
                FORM_EDIT(test, loc)
        
        with col33:
            if st.button(label='➖ DEL TEST', use_container_width=True):
                del DB['TEST_LIST'][loc]
                try:
                    SQL_UPDATE_DB("TEMPLATES", ID, DB)
                    st.session_state.TEMPLATES += 1
                    st.rerun()
                except Exception as e:
                    INFOBOX(e)

        st.text("")
        tbl_cal_test = st.data_editor(
            data=pd.DataFrame(test.CALIBRATION, columns=[field.name for field in TEMPLATE.MEASURE]),
            use_container_width=True,
            hide_index=True,
            column_config={field.name: st.column_config.NumberColumn() for field in TEMPLATE.MEASURE}, 
            num_rows='dynamic'
        )
        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_tbl_update'):

            DB["TEST_LIST"][loc]['CALIBRATION=None'] = tbl_cal_test.to_dict()
            print("UPDATE TBL")
            print(DB)
            try:
                SQL_UPDATE_DB("TEMPLATES", ID, DB)
                st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)




## PAGE
## __________________________________________________________________________________________________

SIDEBAR()

st.text('TEMPLATE Id')

col12, col22 = st.columns(2)

with col12:
    TEMPLATE_ID = st.selectbox("TEMPLATE Id", options=SQL_SELECT_COLUMN("TEMPLATES", "Id"), index=None, label_visibility='collapsed')

with col22:
    with st.popover(USUAL_ICONS.EXPANDER.value):
        FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=SQL_SELECT_COLUMN("DEVICE_TYPES", "Id"), index=None)
        FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=SQL_SELECT_COLUMN("MANUFACTURERS", "Id"), index=None)
        FLTR_MODEL = st.selectbox("MODEL", options=SQL_SELECT_COLUMN("MODELS", "Id"), index=None)

if TEMPLATE_ID:
    SQL = SQL_BY_ROW("TEMPLATES", "Id", TEMPLATE_ID)
    # st.json(SQL)
    CURRENT_TEMPLATE = TEMPLATE.TypeDict(**SQL[0])
    
    ## DB DATA
    CURRENT_DB: dict = None
    if isinstance(CURRENT_TEMPLATE["DB"], str):
        try:
            CURRENT_DB = json.loads(CURRENT_TEMPLATE["DB"])
        except:
            CURRENT_DB = dict()
    elif isinstance(CURRENT_TEMPLATE["DB"], dict):
        CURRENT_DB = CURRENT_TEMPLATE["DB"]
    else:
        CURRENT_DB = dict()


    ## INFO
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('INFO:', divider='blue')

    INFO_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["INFO"])


    ## TEST LIST
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('TEST LIST:', divider='blue')

    if not CURRENT_DB.get("TEST_LIST"):
        CURRENT_DB["TEST_LIST"] = []

    selected = TEST_EDITOR(TEMPLATE_ID, CURRENT_DB)
    # st.write(selected)


    ## PYDATA
    ## __________________________________________________________________________________________________

    st.text("")
    st.text("")
    st.subheader('PYDATA:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ PYDATA](#pydata)
    # """, unsafe_allow_html=True)

    if not CURRENT_TEMPLATE["PYDATA"]:
        CURRENT_TEMPLATE["PYDATA"] = str()
    
    PYDATA_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["PYDATA"])


    ## DB DATA JSON
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 DB DATA:]''')
    st.subheader('JSON DB DATA:', divider='blue')
    
    DB_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["DB"])




## Dataframe selections / https://docs.streamlit.io/develop/api-reference/data/st.dataframe
## __________________________________________________________________________________________________

# if "df" not in st.session_state:
#     st.session_state.df = pd.DataFrame(
#         np.random.randn(12, 5), columns=["a", "b", "c", "d", "e"]
#     )

# event = st.dataframe(
#     st.session_state.df,
#     key="data",
#     on_select="rerun",
#     selection_mode=["multi-row", "multi-column"],
# )

# event.selection