import streamlit as st
from menus import *

import os
import pandas as pd

from flexical.database import tables, table_db #, enum_to_typedDict
from flexical.report import REPORT
from pycalibration.calibration import RESULTS

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
    
    ## DB DATA
    CURRENT_DB: dict = None
    # st.write(CURRENT_TEMPLATE["DB"])
    if isinstance(CURRENT_PROCEDURE[tables.PROCEDURES.DB.name], str):
        # st.write('str')
        try:
            CURRENT_DB = json.loads(CURRENT_PROCEDURE[tables.PROCEDURES.DB.name])
        except:
            CURRENT_DB = dict()
    elif isinstance(CURRENT_PROCEDURE[tables.PROCEDURES.DB.name], dict):
        # st.write('dict')
        CURRENT_DB = CURRENT_PROCEDURE[tables.PROCEDURES.DB.name]
    else:
        # st.write('nope')
        CURRENT_DB = dict()

    st.text('')
    tab_info, tab_testlist, tab_scope, tab_pydata = st.tabs([':material/info: INFO', ':material/lists: TEST', ':material/arrow_range: SCOPE *CMC', ':material/developer_mode: PYDATA'])


    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.INFO.name])

    
    ## TEST
    ## __________________________________________________________________________________________________

    with tab_testlist:

        tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE[tables.PROCEDURES.TITLE.name])
        
        result_types = [result.name for result in RESULTS.TYPES]
        result_type = st.selectbox(
            'TYPE OF RESULT', 
            options=result_types, 
            label_visibility='visible', 
            index=result_types.index(CURRENT_DB[table_db.PROCEDURES.REPORT.name]['RESULT_TYPE'])
            )
        
        abs_values = st.toggle('ABSOLUTE VALUES', value=CURRENT_DB[table_db.PROCEDURES.REPORT.name]['ABSOLUTE_VALUES'])

        CURRENT_REPORT = CURRENT_DB[table_db.PROCEDURES.REPORT.name]

        st.text("TEST REPORT")

        with st.container(border=True):
            TESTREPORT = REPORT.TESTREPORT.format(**CURRENT_REPORT['TESTREPORT'])
            # TESTREPORT = REPORT.TESTREPORT.format(CURRENT_DB[table_db.PROCEDURES.REPORT.name][REPORT.TESTREPORT.])
            
            st.text_input(REPORT.TESTREPORT.fields.PARAMETERS.name, value=TESTREPORT.PARAMETERS)
            st.text_input(REPORT.TESTREPORT.fields.MEASUREMENT.name, value=TESTREPORT.MEASUREMENT)
            st.text_input(REPORT.TESTREPORT.fields.UNCERTAINTY.name, value=TESTREPORT.UNCERTAINTY)
            st.text_input(REPORT.TESTREPORT.fields.LIMIT_OF_ERROR.name, value=TESTREPORT.LIMIT_OF_ERROR)
            st.write(CURRENT_REPORT)
        
        st.text("MEASUREMENT UNITS")
        with st.container(border=True):
            for field in REPORT.MEASUREMENT_UNITS.fields:
                st.text_input(field.name)

        # st.line_chart()
        # st.json(CURRENT_DB)


    ## PYDATA
    ## __________________________________________________________________________________________________

    with tab_pydata:
        if not CURRENT_PROCEDURE["PYDATA"]:
            CURRENT_PROCEDURE["PYDATA"] = str()
        PYDATA_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.PYDATA.name])
