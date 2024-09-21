import streamlit as st
from menus import *
from db import *
import json
import pandas as pd
from flexical.database import tables, table_db

## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None


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
    CURRENT_DB = json.loads(CURRENT_MODEL[tables.MODELS.DB.name])
    st.json(CURRENT_MODEL, expanded=False)
    

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
        st.write(CURRENT_DB[table_db.MODELS.SPECIFICATIONS.name])
