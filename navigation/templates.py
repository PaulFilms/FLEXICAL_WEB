import streamlit as st
from menus import *
from db import *

import os, json
from enum import Enum, auto
from typing import TypedDict
import pandas as pd
import numpy as np

from pycalibration.calibration import CALIBRATION
from flexical.database import views

class TEMPLATE:

    class TypeDict(TypedDict):
        Id: str
        MODEL_ID: str
        VARSION: str
        INFO: str
        DB: dict
        PYDATA: str

    class MEASURE(Enum):
        RANGE_TX = 0
        RANGE = auto()
        VALUE1 = auto()
        VALUE2 = auto()

if 'role' not in st.session_state:
    st.session_state.role = None

if 'filter' not in st.session_state:
    st.session_state.filter = None

if 'TEMPLATES' not in st.session_state:
    st.session_state.TEMPLATES = 1

# @st.cache_resource
# def sql_templates_id(count: int):
#     # print(f"SQL {table} ({count}):", get_firm())
#     return supabase.table('PROCEDURES').select('Id').order("Id").execute().data


## MENU
## __________________________________________________________________________________________________

def TEST_EDITOR(ID: str, DB: dict) -> None:
    procedures = sql_column("PROCEDURES", "Id", st.session_state.TEMPLATES)

    @st.dialog(title='✏️ EDITOR', width='small')
    def FORM_NEW():
        PROCEDURE_ID = st.selectbox("PROCEDURE Id *", options=procedures, index=None)
        title = str()
        if PROCEDURE_ID:
            title = sql_row("PROCEDURES", "Id", PROCEDURE_ID, st.session_state.TEMPLATES)[0]['TITLE']
        TEST = st.text_input("TEST TITLE *", value=title)
        PARAMETERS = st.text_input("TEST PARAMETERS")
        CONFIG = st.text_input("CONFIG & CONNECTIONS")
        INFO = st.text_area("INFO")
        if st.button("➕ INSERT NEW TEST", key='btn_test_ADD'):
            NEW_TEST = CALIBRATION.TEST(TEST, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, CALIBRATION={})
            DB["TEST_LIST"].append(NEW_TEST.toDict())
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    @st.dialog(title='✏️ EDITOR', width='small')
    def FORM_EDIT(TEST: CALIBRATION.TEST, loc):
        indx = None
        if TEST.PROCEDURE_ID in procedures:
            indx = procedures.index(TEST.PROCEDURE_ID)
        PROCEDURE_ID = st.selectbox("PROCEDURE Id", options=procedures, index=indx)
        TITLE = st.text_input("TEST TITLE *", value=TEST.TEST)
        PARAMETERS = st.text_input("TEST PARAMETERS", value=TEST.PARAMETERS)
        CONFIG = st.text_input("CONFIG & CONNECTIONS", value=TEST.CONFIG)
        INFO = st.text_area("INFO", value=TEST.INFO)
        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_test_update'):
            EDIT_TEST = CALIBRATION.TEST(TITLE, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, TEST.CALIBRATION)
            DB["TEST_LIST"][loc] = EDIT_TEST.toDict()
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    ## TABLE TEST
    DATAFRAME = pd.DataFrame(DB['TEST_LIST'], columns=['TEST', 'PARAMETERS', 'CONFIG', 'INFO', 'PROCEDURE_ID'])

    col12, col22 = st.columns([9,1])

    with col12:
        TBL_TEST = st.dataframe(
            data=DATAFRAME, 
            hide_index=True,
            on_select="rerun", # Con esta opcion aparece el selector de fila
            selection_mode=['single-row'], # "multi-column" "multi-row"
            use_container_width=True,
        )
    
    with col22:
        with st.popover(USUAL_ICONS.EXPANDER.value):
            if st.button(label='➕ ADD TEST', use_container_width=True):
                FORM_NEW()

            if len(TBL_TEST.selection.rows) == 1:
                loc = TBL_TEST.selection.rows[0]
                test = CALIBRATION.TEST(**DB["TEST_LIST"][loc])

                if st.button(label='✏️ EDIT TEST', use_container_width=True):
                    FORM_EDIT(test, loc)
                
                if st.button(label='➖ DEL TEST', use_container_width=True):
                    del DB['TEST_LIST'][loc]
                    try:
                        sql_update_db("TEMPLATES", ID, DB)
                        # st.session_state.TEMPLATES += 1
                        st.rerun()
                    except Exception as e:
                        INFOBOX(e)
                
                if loc > 0:
                    if st.button(label=USUAL_ICONS.UP.value, use_container_width=True):
                        DB['TEST_LIST'].insert(loc-1, DB['TEST_LIST'].pop(loc))
                        sql_update_db("TEMPLATES", ID, DB)
                        # st.session_state.TEMPLATES += 1
                        st.rerun()
                
                if loc < len(DB['TEST_LIST'])-1:
                    if st.button(label=USUAL_ICONS.DOWN.value, use_container_width=True):
                        DB['TEST_LIST'].insert(loc+1, DB['TEST_LIST'].pop(loc))
                        sql_update_db("TEMPLATES", ID, DB)
                        # st.session_state.TEMPLATES += 1
                        st.rerun()

    if len(TBL_TEST.selection.rows) == 1:
        st.text("")
        DF_CALIBRATION = pd.DataFrame(test.CALIBRATION, columns=[field.name for field in TEMPLATE.MEASURE])
        DF_CALIBRATION['RANGE_TX'] = DF_CALIBRATION['RANGE_TX'].astype(str)
        DF_CALIBRATION['RANGE'] = DF_CALIBRATION['RANGE'].astype(float)
        DF_CALIBRATION['VALUE1'] = DF_CALIBRATION['VALUE1'].astype(float)
        DF_CALIBRATION['VALUE2'] = DF_CALIBRATION['VALUE2'].astype(float)
        DF_CALIBRATION = DF_CALIBRATION.reset_index()
        del DF_CALIBRATION['index']

        st.write('TEST MEASURES:')

        tbl_cal_test = st.data_editor(
            # data=pd.DataFrame(test.CALIBRATION, columns=[field.name for field in TEMPLATE.MEASURE]),
            data=DF_CALIBRATION,
            use_container_width=True,
            hide_index=True,
            column_config={
                'RANGE_TX': st.column_config.TextColumn(default=""),
            }, 
            num_rows='dynamic'
        )
        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_tbl_update'):
            tbl_cal_test['RANGE_TX'] = tbl_cal_test['RANGE_TX'].replace({False: str(), np.nan: str()})
            DB["TEST_LIST"][loc]['CALIBRATION'] = tbl_cal_test.to_dict()
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

@st.cache_resource
def sql_templates_filter(count: int):
    data = (
        supabase.table('TEMPLATES_VIEW')
        .select(
            views.TEMPLATES_VIEW.Id.name,
            views.TEMPLATES_VIEW.DEVICE_TYPE.name,
            views.TEMPLATES_VIEW.MANUFACTURER.name,
            views.TEMPLATES_VIEW.MODEL.name,
        )
        .order('Id')
        .execute().data
    )
    return data

@st.dialog('FILTERS', width='small')
def FILTERS(dataFrame: pd.DataFrame):
    FLTR_DEVICE: str = None
    FLTR_MANUFACTURER: str = None
    FLTR_MODEL: str = None
    FLTR_ID: str = None
    
    def get_filter():
        df_filtered = DATAFRAME.copy()
        if FLTR_DEVICE: 
            df_filtered = df_filtered[df_filtered['DEVICE_TYPE']==FLTR_DEVICE]
        if FLTR_MANUFACTURER: 
            df_filtered = df_filtered[df_filtered['MANUFACTURER']==FLTR_MANUFACTURER]
        if FLTR_MODEL: 
            df_filtered = df_filtered[df_filtered['MODEL']==FLTR_MODEL]
        if FLTR_ID: 
            df_filtered = df_filtered[df_filtered['Id']==FLTR_ID]

        return df_filtered

    FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=get_filter()['DEVICE_TYPE'].unique().tolist(), index=None)
    FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=get_filter()['MANUFACTURER'].unique().tolist(), index=None)
    FLTR_MODEL = st.selectbox("MODEL", options=get_filter()['MODEL'].unique().tolist(), index=None)
    FLTR_ID = st.selectbox("Id", options=get_filter()['Id'].unique().tolist(), index=None)

    st.text('')
    st.text('')
    if st.button('SUBMIT', use_container_width=True):
        if not FLTR_ID or FLTR_ID == str():
            INFOBOX("PLEASE, SELECT A VALID TEMPLATE Id")
        else:
            st.session_state.filter = FLTR_ID
            st.rerun()



## PAGE
## __________________________________________________________________________________________________

DATAFRAME = pd.DataFrame(sql_templates_filter(st.session_state.TEMPLATES))

st.text('SELECT TEMPLATE Id:')

col12, col22 = st.columns(2)

with col12:
    holder_template = st.empty()
    TEMPLATE_ID = holder_template.selectbox("TEMPLATE Id", options=DATAFRAME['Id'].to_list(), index=None, label_visibility='collapsed')

with col22:
    btn_filters = st.button(':material/filter: FILTERS')

if btn_filters:
    FILTERS(DATAFRAME)

if st.session_state.filter:
    TEMPLATE_ID = holder_template.selectbox("TEMPLATE Id", options=DATAFRAME['Id'].to_list(), index=DATAFRAME['Id'].to_list().index(st.session_state.filter), label_visibility='collapsed')
    st.session_state.filter = None


if TEMPLATE_ID:
    SQL = sql_row('TEMPLATES', 'Id', TEMPLATE_ID, st.session_state.TEMPLATES)
    # st.write(SQL)
    CURRENT_TEMPLATE = TEMPLATE.TypeDict(**SQL[0])
    # CURRENT_TEMPLATE = DATAFRAME[DATAFRAME['Id']==TEMPLATE_ID].iloc[0]
    # CURRENT_TEMPLATE = TEMPLATE.TypeDict(**dict(CURRENT_TEMPLATE))
    # st.write(CURRENT_TEMPLATE)
    # st.write(CURRENT_TEMPLATE['Id'])

    ## DB DATA
    CURRENT_DB: dict = None
    # st.write(CURRENT_TEMPLATE["DB"])
    if isinstance(CURRENT_TEMPLATE["DB"], str):
        # st.write('str')
        try:
            CURRENT_DB = json.loads(CURRENT_TEMPLATE["DB"])
        except:
            CURRENT_DB = dict()
    elif isinstance(CURRENT_TEMPLATE["DB"], dict):
        # st.write('dict')
        CURRENT_DB = CURRENT_TEMPLATE["DB"]
    else:
        # st.write('nope')
        CURRENT_DB = dict()
    # st.write(CURRENT_DB)

    # st.json(CURRENT_TEMPLATE["DB"])

#     # JSON = json.loads(CURRENT_TEMPLATE['DB'])
#     # st.json(JSON)

    st.text('')
    tab_info, tab_testlist, tab_pydata = st.tabs([':material/info: INFO', ':material/lists: TEST', ':material/developer_mode: PYDATA'])

    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:

        # st.text("") # SEPARATOR
        # # st.markdown(''':blue-background[💊 CMC:]''')
        # st.subheader('INFO:', divider='blue')

        MD_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["INFO"])



    ## TEST LIST
    ## __________________________________________________________________________________________________

    with tab_testlist:

        # st.text("") # SEPARATOR
        # # st.markdown(''':blue-background[💊 CMC:]''')
        # st.subheader('TEST LIST:', divider='blue')

        if not CURRENT_DB.get("TEST_LIST"):
            CURRENT_DB["TEST_LIST"] = []

        # st.write(CURRENT_DB["TEST_LIST"])
        selected = TEST_EDITOR(TEMPLATE_ID, CURRENT_DB)
        # st.write(selected)


    ## PYDATA
    ## __________________________________________________________________________________________________

    with tab_pydata:

        # st.text("")
        # st.text("")
        # st.subheader('PYDATA:', divider='blue')

        # st.sidebar.markdown("""
        # [➡️ PYDATA](#pydata)
        # """, unsafe_allow_html=True)

        if not CURRENT_TEMPLATE["PYDATA"]:
            CURRENT_TEMPLATE["PYDATA"] = str()
        
        PYDATA_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["PYDATA"])


    ## DB DATA JSON
    ## __________________________________________________________________________________________________

    # st.text("") # SEPARATOR
    # st.text("") # SEPARATOR
    # # st.markdown(''':blue-background[💊 DB DATA:]''')
    # st.subheader('JSON DB DATA:', divider='blue')
    
    # DB_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["DB"])

