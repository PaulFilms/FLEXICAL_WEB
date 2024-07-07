'''
FLEXICAL v3 | CMC

'''

## PYTHON LIBRARIES
import os

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


## MENU
## __________________________________________________________________________________________________



## PAGE
## __________________________________________________________________________________________________

SIDEBAR()

st.text('MODEL SERIES Id')

col12, col22 = st.columns(2)

with col12:
    SERIES_ID = st.selectbox("TEMPLATE Id", options=[], index=None, label_visibility='collapsed')



## PROCEDURES
## __________________________________________________________________________________________________

st.text("")
st.text("")
st.subheader('PROCEDURES:', divider='blue')

col12, col22 = st.columns(2)

with col12:
    procedures = ['POLLA', "LOCA"]
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
        pass

if CURRENT_PROCEDURE:

    ## MODELS
    ## __________________________________________________________________________________________________

    # st.text("")
    # st.text("")
    # st.subheader('MODELS:', divider='blue')
    st.markdown(''':blue-background[💊 MODELS:]''')

    col12, col22 = st.columns(2)

    with col12:
        models = ['IBIZA', "TOLEDO"]
        model = st.dataframe(
            data=pd.DataFrame(models, columns=['VALUE']),
            use_container_width=True,
            hide_index=True,
            on_select="rerun", # Con esta opcion aparece el selector de fila
            selection_mode=['single-row'], # "multi-column" "multi-row"
        )

    column_config={
        "RANGE": st.column_config.NumberColumn(),
        'VALUE1': st.column_config.NumberColumn(),
        'VALUE2': st.column_config.NumberColumn()
    }

    st.markdown(''':blue-background[💊 CMC:]''')
    st.data_editor(
        data=pd.DataFrame(columns=[field for field in column_config.keys()]), 
        use_container_width=True, 
        hide_index=True,
        num_rows='dynamic',
        column_config=column_config
    )