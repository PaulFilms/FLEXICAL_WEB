import streamlit as st
from menus import *
from db import *

import os, json
from typing import TypedDict
import pandas as pd

class TEMPLATE:

    class TypeDict(TypedDict):
        Id: str
        MODEL_ID: str
        VARSION: str
        INFO: str
        DB: dict
        PYDATA: str

if 'tbl_templates_count' not in st.session_state:
    st.session_state.tbl_templates_count = 1

# @st.cache_resource
# def sql_templates_id(count: int):
#     # print(f"SQL {table} ({count}):", get_firm())
#     return supabase.table('PROCEDURES').select('Id').order("Id").execute().data

SQL = sql_table('TEMPLATES', st.session_state.tbl_templates_count)
DATAFRAME = pd.DataFrame(SQL)

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
    st.write(CURRENT_TEMPLATE["DB"])
    if isinstance(CURRENT_TEMPLATE["DB"], str):
        st.write('str')
        try:
            CURRENT_DB = json.loads(CURRENT_TEMPLATE["DB"])
        except:
            CURRENT_DB = dict()
    elif isinstance(CURRENT_TEMPLATE["DB"], dict):
        st.write('dict')
        CURRENT_DB = CURRENT_TEMPLATE["DB"]
    else:
        st.write('nope')
        CURRENT_DB = dict()
    st.write(CURRENT_DB)

    # st.json(CURRENT_TEMPLATE["DB"])

    # JSON = json.loads(CURRENT_TEMPLATE['DB'])
    # st.json(JSON)