import streamlit as st
from menus import *
from db import *

import os, json
from enum import Enum, auto
from typing import TypedDict
import pandas as pd

from pycalibration.calibration import CALIBRATION

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

if 'TEMPLATES' not in st.session_state:
    st.session_state.TEMPLATES = 1

# @st.cache_resource
# def sql_templates_id(count: int):
#     # print(f"SQL {table} ({count}):", get_firm())
#     return supabase.table('PROCEDURES').select('Id').order("Id").execute().data


## MENU
## __________________________________________________________________________________________________

def TEST_EDITOR(ID: str, DB: dict) -> None:
    procedures = sql_column("PROCEDURES", "Id")

    @st.dialog(title='✏️ EDITOR', width='small')
    def FORM_NEW():
        PROCEDURE_ID = st.selectbox("PROCEDURE Id *", options=procedures, index=None)
        title = str()
        if PROCEDURE_ID:
            title = sql_row("PROCEDURES", "Id", PROCEDURE_ID)[0]['TITLE']
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
            DB["TEST_LIST"][loc]['CALIBRATION'] = tbl_cal_test.to_dict()
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

def get_filter() -> pd.DataFrame:
    df_filtered = DATAFRAME.copy()
    # for filter in [FLTR_DEVICE, FLTR_MANUFACTURER, FLTR_ID]:
    #     if filter == None or 
    # if FLTR_DEVICE:
    #     df_filtered = df_filtered[df_filtered['DEVICE_TYPE']==FLTR_DEVICE]
    # if FLTR_MANUFACTURER:
    #     df_filtered = df_filtered[df_filtered['MANUFACTURER']==FLTR_MANUFACTURER]
    if FLTR_ID:
        df_filtered = df_filtered[df_filtered['Id']==FLTR_ID]
    return df_filtered

## PAGE
## __________________________________________________________________________________________________

SQL = sql_table('TEMPLATES', st.session_state.TEMPLATES)
DATAFRAME = pd.DataFrame(SQL)

with st.expander('FILTERS'): # , use_container_width=True
    # FsNUFACTURER = st.selectbox("MANUFACTURER", options=DATAFRAME['MANUFACTURER'].unique().tolist(), index=None)
    # FLTR_ID = st.selectbox("Id", options=DATAFRAME['Id'].unique().tolist(), index=None)

    # if FLTR_ID:
    #     TEMPLATE_ID = ho
    col13, col23, col33 = st.columns(3)
    with col13:
        st.button('TYPE DEVICE', use_container_width=True)
    with col23:
        st.button('MANUFACTURER', use_container_width=True)
    with col33:
        st.button('MODEL', use_container_width=True)


col12, col22 = st.columns(2)

with col12:
    holder_template = st.empty()
    TEMPLATE_ID = holder_template.selectbox("TEMPLATE Id", options=DATAFRAME['Id'].to_list(), index=None, label_visibility='collapsed')

if TEMPLATE_ID:
    # CURRENT_TEMPLATE = TEMPLATE.TypeDict(**SQL[0])
    CURRENT_TEMPLATE = DATAFRAME[DATAFRAME['Id']==TEMPLATE_ID].iloc[0]
    CURRENT_TEMPLATE = TEMPLATE.TypeDict(**dict(CURRENT_TEMPLATE))
    # st.write(CURRENT_TEMPLATE)
    # st.write(type(CURRENT_TEMPLATE))
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

    # JSON = json.loads(CURRENT_TEMPLATE['DB'])
    # st.json(JSON)



    ## INFO
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('INFO:', divider='blue')

    MD_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["INFO"])



    ## TEST LIST
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('TEST LIST:', divider='blue')

    if not CURRENT_DB.get("TEST_LIST"):
        CURRENT_DB["TEST_LIST"] = []

    # st.write(CURRENT_DB["TEST_LIST"])
    selected = TEST_EDITOR(TEMPLATE_ID, CURRENT_DB)
    # st.write(selected)