import streamlit as st
from menus import *
from db import *

from time import sleep
import json
from typing import Dict

import pandas as pd
from flexical.database import tables, table_db



## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'filter' not in st.session_state:
    st.session_state.filter = None

if 'MODELS' not in st.session_state:
    st.session_state.MODELS = 1



## TOOLS
## __________________________________________________________________________________________________

@st.cache_resource
def sql_models_filter(count: int):
    data = (
        supabase.table('MODELS')
        .select(
            tables.MODELS.Id.name,
            tables.MODELS.DEVICE_TYPE.name,
            tables.MODELS.MANUFACTURER.name,
            tables.MODELS.MODEL.name,
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
    
    def get_filter():
        df_filtered = dataFrame.copy()
        if FLTR_DEVICE: 
            df_filtered = df_filtered[df_filtered['DEVICE_TYPE']==FLTR_DEVICE]
        if FLTR_MANUFACTURER: 
            df_filtered = df_filtered[df_filtered['MANUFACTURER']==FLTR_MANUFACTURER]
        if FLTR_MODEL: 
            df_filtered = df_filtered[df_filtered['MODEL']==FLTR_MODEL]

        return df_filtered

    FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=get_filter()['DEVICE_TYPE'].unique().tolist(), index=None)
    FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=get_filter()['MANUFACTURER'].unique().tolist(), index=None)
    FLTR_MODEL = st.selectbox("MODEL", options=get_filter()['MODEL'].unique().tolist(), index=None)

    st.text('')
    st.text('')
    if st.button('SUBMIT', use_container_width=True):
        if not FLTR_MODEL or FLTR_MODEL == str():
            INFOBOX("PLEASE, SELECT A VALID MODEL")
        else:
            st.session_state.filter = dataFrame[dataFrame['MODEL']==FLTR_MODEL]['Id'].iloc[0]
            st.rerun()

tbl_specification_config = {
        'RANGE1_MIN': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'RANGE1_MAX': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'RANGE2_MIN': st.column_config.NumberColumn(format="%.2e", default=None),
        'RANGE2_MAX': st.column_config.NumberColumn(format="%.2e", default=None),
        'RESOLUTION': st.column_config.NumberColumn(format="%.2e", default=0.0), #, default=0.0), format="%.2e"
        'C1': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C2': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C3': st.column_config.NumberColumn(format="%.2e", default=None),
        'EVALUATION': st.column_config.TextColumn(default='''(VALUE1*C1*1e1)+(C2*1e1)''', width='small'),
    }



## PAGE
## __________________________________________________________________________________________________

DATAFRAME = pd.DataFrame(sql_models_filter(st.session_state.MODELS))

st.text('✏️ SELECT MODEL Id')

col12, col22 = st.columns(2)

with col12:
    holder_model = st.empty()
    # MODEL_ID = holder_model.text_input(label="✏️ ENTER MODEL Id", value="", label_visibility='collapsed')
    MODEL_ID = holder_model.selectbox("MODEL Id", options=DATAFRAME['Id'].to_list(), index=None, label_visibility='collapsed')

with col22:
    btn_filters = st.button(':material/filter: FILTERS')

if btn_filters:
    FILTERS(DATAFRAME)

if st.session_state.filter:
    MODEL_ID = holder_model.selectbox("MODEL Id", options=DATAFRAME['Id'].to_list(), index=DATAFRAME['Id'].to_list().index(st.session_state.filter), label_visibility='collapsed')
    st.session_state.filter = None

if MODEL_ID:
    CURRENT_MODEL = sql_row('MODELS', 'Id', MODEL_ID, st.session_state.MODELS)
    # CURRENT_DB: Dict[str, dict] = json.loads(CURRENT_MODEL[tables.MODELS.DB.name])
    CURRENT_DB: Dict[str, dict] = CURRENT_MODEL[tables.MODELS.DB.name]
    # st.json(CURRENT_MODEL, expanded=False)
    

    ## TABS
    ## __________________________________________________________________________________________________

    st.text('')
    tab_info, tab_specifications = st.tabs([':material/info: INFO', ':material/arrow_range: SPECIFICATIONS'])
    # , tab_testlist, tab_standards, tab_scope, tab_pydata
    # , ':material/lists: TEST', ':material/microwave: STANDARDS', , ':material/developer_mode: PYDATA'


    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("MODELS", MODEL_ID, CURRENT_MODEL[tables.MODELS.INFO.name])

    
    with tab_specifications:
        # st.write(CURRENT_DB[table_db.MODELS.SPECIFICATIONS.name])
        
        ## PROCEDURES
        col12, col22 = st.columns(2)

        with col12:
            # COLUMN_NAME = "PROCEDURE Id"
            # MODEL_PROCEDURES = pd.DataFrame(list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()), columns=[COLUMN_NAME])
            # TBL_PROCEDURES, CURRENT_PROCEDURE = DATAFRAME_LIST(MODEL_PROCEDURES, COLUMN_NAME) # st.session_state.MODEL_PROCEDURES
            procedures = list(CURRENT_DB['SPECIFICATIONS'].keys())
            procedure = st.dataframe(
                data=pd.DataFrame(procedures, columns=['VALUE']),
                use_container_width=True,
                hide_index=True,
                on_select="rerun", # Con esta opcion aparece el selector de fila
                selection_mode=['single-row'], # "multi-column" "multi-row"
            )
            if len(procedure.selection.rows):
                CURRENT_PROCEDURE = procedures[procedure.selection.rows[0]]
            else:
                CURRENT_PROCEDURE = None

        with col22:
            with st.popover(label=chr(8801)):
                with st.container(border=True):
                    if 'PROCEDURES' not in st.session_state:
                        st.session_state.PROCEDURES = 1
                    procedures_list = sql_column('PROCEDURES', 'Id', st.session_state.PROCEDURES)
                    procedure_Id = st.selectbox("PROCEDURE Id", options=[proc for proc in procedures_list])
                    if st.button(label='➕ INSERT PROCEDURE', use_container_width=True):
                        if procedure_Id in list(CURRENT_DB['SPECIFICATIONS'].keys()):
                            st.warning(f"< {procedure_Id} > It's already in the list", icon="⚠️")
                        else:
                            CURRENT_DB['SPECIFICATIONS'][procedure_Id] = {}
                            sql_update_db('MODELS', MODEL_ID, CURRENT_DB)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                    if CURRENT_PROCEDURE and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                        def DELETE_PROCEDURE():
                            CURRENT_DB['SPECIFICATIONS'].pop(CURRENT_PROCEDURE)
                            # SQL_UPDATE_DB("MODELS", MODEL_ID, st.session_state.DB_DATA)
                            st.rerun()

                        YESNOBOX(f"DO YOU WANT TO DELETE THIS PROCEDURE?\n< {CURRENT_PROCEDURE} >", DELETE_PROCEDURE)

        # FUNC(CURRENT_PROCEDURE)
        st.text("") # SEPARATOR
        st.text("") # SEPARATOR

        # if len(procedure.selection.rows):
        if CURRENT_PROCEDURE:
            DF_SPEC = pd.DataFrame(CURRENT_DB['SPECIFICATIONS'].get(CURRENT_PROCEDURE), columns=list(tbl_specification_config.keys()))
            DF_SPEC['RESOLUTION'] = DF_SPEC['RESOLUTION'].astype(float)

            TBL_SPECIFICATION, BTN_UPDATE = TBL_EDITOR(DF_SPEC)
            if BTN_UPDATE:
                if len(TBL_SPECIFICATION) == 0:
                    CURRENT_DB['SPECIFICATIONS'][CURRENT_PROCEDURE] = {}
                else:
                    CURRENT_DB['SPECIFICATIONS'][CURRENT_PROCEDURE] = TBL_SPECIFICATION.replace(np.nan, None).to_dict()
                sql_update_db('MODELS', MODEL_ID, CURRENT_DB)
                st.toast(body="🏁 SPECIFICATIONS Updated")
                st.rerun()
