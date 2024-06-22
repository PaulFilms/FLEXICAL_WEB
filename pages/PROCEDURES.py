'''
FLEXICAL v3 | PROCEDURES

'''

## PYTHON LIBRARIES
import os
from time import sleep
from typing import TypedDict

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import *
from db import *



## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

if 'PROCEDURES' not in st.session_state:
    st.session_state.PROCEDURES = 1

if 'DB_DATA' not in st.session_state:
    st.session_state.DB_DATA = None


## MENU
## __________________________________________________________________________________________________

class PROCEDURE:
    '''class'''

    class TypeDict(TypedDict):
        Id: str
        TITLE: str
        INFO: str
        DB: dict
        PYDATA: str
        FIRM: str

tbl_cmc_config={
    'RANGE1_MIN': st.column_config.NumberColumn(default=0.0, format="%.2e"), # min_value=-1e-16, max_value=1e16),
    'RANGE1_MAX': st.column_config.NumberColumn(default=0.0, format="%.2e"), # min_value=-1e-16, max_value=1e16),
    'RANGE2_MIN': st.column_config.NumberColumn(default=None,format="%.2e"), # min_value=-1e-16, max_value=1e16),
    'RANGE2_MAX': st.column_config.NumberColumn(default=None,format="%.2e"), # min_value=-1e-16, max_value=1e16),
    'EVALUATION': st.column_config.TextColumn(default="C1 # VALUE1 VALUE2"),
    'C1': st.column_config.NumberColumn(format="%.2e", default=0.0, min_value=-1e-16, max_value=1e16), # 0.0
    'C2': st.column_config.NumberColumn(format="%.2e", default=None, min_value=-1e-16, max_value=1e16), # 0.0
    'C3': st.column_config.NumberColumn(format="%.2e", default=None, min_value=-1e-16, max_value=1e16), # 0.0
}



## PAGE
## __________________________________________________________________________________________________

SIDEBAR()

st.text("PROCEDURE Id")
col12, col22 = st.columns(2)

with col12:
    # print(SQL_PROCEDURES(1))
    PROCEDURE_ID = st.selectbox("🎛️ PROCEDURE Id", options=[procedure['Id'] for procedure in SQL_PROCEDURES(st.session_state.PROCEDURES)], index=None, label_visibility='collapsed')

if PROCEDURE_ID:
    SQL = SQL_BY_ROW('PROCEDURES', "Id", PROCEDURE_ID)

    with col22:
        # BUG
        if st.button("📄 SHOW DOCUMENT", use_container_width=True):
            @st.experimental_dialog("📄 DOCUMENT **INCOMPLETE", width='large')
            def DOCUMENT():
                MD = r'''
                ## PROCEDURE Id
                ---

                Information about procedure


                :blue-background[STANDARDS USED:]
                - Standard 1
                - Standard n

                
                :blue-background[UNCERTAINTY:]

                $$
                u = \sqrt{a^2 + b^2 + c^2}
                $$

                
                :blue-background[CMC:]

                | Column 1      | Column 2      |
                | ------------- | ------------- |
                | Cell 1, Row 1 | Cell 2, Row 1 |
                | Cell 1, Row 2 | Cell 1, Row 2 |

                
                -
                '''
                st.button("PRINT DOCUMENT")
                with st.container(border=True): # height=300, 
                    st.markdown(MD, unsafe_allow_html=True)
            DOCUMENT()

    if len(SQL) != 1:
        st.session_state.DB_DATA = None
        INFOBOX(f"< {PROCEDURE_ID} > don't exits")

    else:
        CURRENT_PROCEDURE = PROCEDURE.TypeDict(**SQL[0])
        CURRENT_DB = CURRENT_PROCEDURE["DB"]
        st.json(CURRENT_PROCEDURE, expanded=False)

        ## DB DATA
        if isinstance(CURRENT_DB, str):
            try:
                st.session_state.DB_DATA = json.loads(CURRENT_DB)
            except:
                st.session_state.DB_DATA = dict()
        elif isinstance(CURRENT_DB, dict):
            st.session_state.DB_DATA = CURRENT_DB
        else:
            st.session_state.DB_DATA = dict()

        ## DATA
        ## __________________________________________________________________________________________________

        st.text("")
        st.text("")
        st.subheader('DATA:', divider='blue')

        tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE["TITLE"])
        # tx_info = st.text_area(label='INFO', value=CURRENT_PROCEDURE["INFO"])
        INFO_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE["INFO"])



        ## REPORT FORMATS
        ## __________________________________________________________________________________________________

        st.text("")
        st.text("")
        st.subheader('REPORT FORMATS:', divider='blue')

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 REPORT FORMATS:]''')

        st.text("REPORT FORMATS")


        ## STANDARDS
        ## __________________________________________________________________________________________________

        st.text("") # SEPARATOR
        # st.markdown(''':blue-background[💊 STANDARDS:]''')
        st.subheader('STANDARDS:', divider='blue')

        if not st.session_state.DB_DATA.get('STANDARDS'):
            st.session_state.DB_DATA['STANDARDS'] = dict()

        col12, col22 = st.columns(2)
        
        with col12:
            PROCEDURE_STANDARDS = pd.DataFrame(list(st.session_state.DB_DATA['STANDARDS'].keys()), columns=["DEVICE TYPE"])
            TBL_STANDARDS, CURRENT_STANDARD = DATAFRAME_LIST(PROCEDURE_STANDARDS, "DEVICE TYPE")

        with col22:
            with st.popover(label=chr(8801)):
                with st.container(border=True):
                    if 'DEVICE_TYPES' not in st.session_state:
                        st.session_state.DEVICE_TYPES = 1
                    device_type = st.selectbox("DEVICE TYPE", options=SQL_SELECT_COLUMN("DEVICE_TYPES", "Id"))
                    if st.button(label='➕ INSERT TYPE', use_container_width=True):
                        if device_type in list(st.session_state.DB_DATA['STANDARDS'].keys()):
                            INFOBOX(f"< {device_type} > It's already in the list")
                        else:
                            st.session_state.DB_DATA['STANDARDS'][device_type] = {}
                            SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                if CURRENT_STANDARD and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                    @st.experimental_dialog(title="❓")
                    def YESNO_int(info: str):
                        st.text(info)
                        col12, col22 = st.columns(2)
                        with col12:
                            if st.button("YES", use_container_width=True):
                                st.session_state.DB_DATA['STANDARDS'].pop(CURRENT_STANDARD)
                                SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
                                st.rerun()
                        with col22:
                            if st.button("NO", use_container_width=True):
                                st.rerun()
                    
                    YESNO_int(f"DO YOU WANT TO DELETE THIS STANDARD?\n< {CURRENT_PROCEDURE} >")



        ## CMC
        ## __________________________________________________________________________________________________

        st.text("") # SEPARATOR
        # st.markdown(''':blue-background[💊 CMC:]''')
        st.subheader('CMC:', divider='blue')

        if not st.session_state.DB_DATA.get('CMC'):
            st.session_state.DB_DATA['CMC'] = dict()

        DF_CMC = pd.DataFrame(st.session_state.DB_DATA['CMC'], columns=list(tbl_cmc_config.keys()))
        TBL_CMC, BTN_UPDATE = TBL_EDITOR(DF_CMC)

        if BTN_UPDATE:
            if len(TBL_CMC) == 0:
                st.session_state.DB_DATA['CMC'] = {}
            else:
                st.session_state.DB_DATA['CMC'] = TBL_CMC.to_dict()
            SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
            st.toast("🏁 CMC Updated")



        ## PYDATA
        ## __________________________________________________________________________________________________

        st.text("")
        st.text("")
        st.subheader('PYDATA:', divider='blue')

        # st.sidebar.markdown("""
        # [➡️ PYDATA](#pydata)
        # """, unsafe_allow_html=True)

        if CURRENT_PROCEDURE["PYDATA"] == None:
            CURRENT_PROCEDURE["PYDATA"] = str()

        PYDATA_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE["PYDATA"])


        ## DB DATA JSON
        ## __________________________________________________________________________________________________

        st.text("") # SEPARATOR
        st.text("") # SEPARATOR
        # st.markdown(''':blue-background[💊 DB DATA:]''')
        st.subheader('JSON DB DATA:', divider='blue')

        DB_EDITOR("MODELS", PROCEDURE_ID, st.session_state.DB_DATA)
