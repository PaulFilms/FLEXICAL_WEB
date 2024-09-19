import streamlit as st
from menus import *

import os
import pandas as pd

from flexical.database import tables, enum_to_typedDict

## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'PROCEDURES' not in st.session_state:
    st.session_state.PROCEDURES = 1


## PAGE
## __________________________________________________________________________________________________

# st.logo(os.path.join(path_resources, 'LOGO2.svg'))
# st.title('PROCEDURES PAGE')

# DATAFRAME = pd.DataFrame(sql_templates_filter(st.session_state.TEMPLATES))
# SQL = sql_column('PROCEDURES', tables.CMC.Id.name, st.session_state.PROCEDURES)
# st.write(SQL)

st.text('SELECT PROCEDURE Id:')

col12, col22 = st.columns(2)

with col12:
    # print(SQL_PROCEDURES(1))
    SQL = sql_column('PROCEDURES', tables.CMC.Id.name, st.session_state.PROCEDURES)
    PROCEDURE_ID = st.selectbox("🎛️ PROCEDURE Id", options=[value for value in SQL], index=None, label_visibility='collapsed')
    # for f in SQL:
    #     st.write(f)


if PROCEDURE_ID:
    CURRENT_PROCEDURE = sql_row('PROCEDURES', 'Id', PROCEDURE_ID, st.session_state.PROCEDURES)[0]
    CURRENT_PROCEDURE = {field.name: CURRENT_PROCEDURE[field.name] for field in tables.PROCEDURES}
    
    # st.write(SQL)

    st.text('')
    tab_info, tab_testlist, tab_pydata = st.tabs([':material/info: INFO', ':material/lists: TEST', ':material/developer_mode: PYDATA'])


    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.INFO.name])



    ## PYDATA
    ## __________________________________________________________________________________________________

    with tab_pydata:
        if not CURRENT_PROCEDURE["PYDATA"]:
            CURRENT_PROCEDURE["PYDATA"] = str()
        PYDATA_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.PYDATA.name])
