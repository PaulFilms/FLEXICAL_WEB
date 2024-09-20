import streamlit as st
from menus import *

import os
import pandas as pd

from flexical.database import tables, table_db #, enum_to_typedDict
from flexical.report import REPORT
from pycalibration.calibration import RESULTS
from pycalibration.units import UNITS

## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'PROCEDURES' not in st.session_state:
    st.session_state.PROCEDURES = 1


## SESSION STATES
## __________________________________________________________________________________________________

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
    # st.write(CURRENT_DB)

    st.text('')
    tab_info, tab_testlist, tab_scope, tab_pydata = st.tabs([':material/info: INFO', ':material/lists: TEST', ':material/arrow_range: SCOPE *CMC', ':material/developer_mode: PYDATA'])


    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.INFO.name])

    
    ## TEST
    ## __________________________________________________________________________________________________

    with tab_testlist:
        
        st.text('')
        tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE[tables.PROCEDURES.TITLE.name])
        
        st.text('')
        result_types = [result.name for result in RESULTS.TYPES]
        result_type = st.selectbox(
            'TYPE OF RESULT', 
            options=result_types, 
            label_visibility='visible', 
            index=result_types.index(CURRENT_DB[table_db.PROCEDURES.REPORT.name]['RESULT_TYPE'])
            )
        
        abs_values = st.toggle('ABSOLUTE VALUES', value=CURRENT_DB[table_db.PROCEDURES.REPORT.name]['ABSOLUTE_VALUES'])

        CURRENT_REPORT = CURRENT_DB[table_db.PROCEDURES.REPORT.name]

        st.text('')
        st.text('')
        # st.text("TEST REPORT")
        # with st.container(border=True):
        with st.expander('TEST REPORT', icon=':material/lab_profile:'):
            st.text('')
            TESTREPORT = REPORT.TESTREPORT.format(**CURRENT_REPORT['TESTREPORT'])
            # TESTREPORT = REPORT.TESTREPORT.format(CURRENT_DB[table_db.PROCEDURES.REPORT.name][REPORT.TESTREPORT.])
            
            st.text_input(REPORT.TESTREPORT.fields.PARAMETERS.name, value=TESTREPORT.PARAMETERS, placeholder='RANGE: {RANGE} V | NOMINAL: {VALUE1} V')
            st.text_input(REPORT.TESTREPORT.fields.MEASUREMENT.name, value=TESTREPORT.MEASUREMENT, placeholder='{DEVIATION} V')
            st.text_input(REPORT.TESTREPORT.fields.UNCERTAINTY.name, value=TESTREPORT.UNCERTAINTY, placeholder='{UNCERTAINTY:.1E} V')
            st.text_input(REPORT.TESTREPORT.fields.LIMIT_OF_ERROR.name, value=TESTREPORT.LIMIT_OF_ERROR, placeholder='± {SPECIFICATION:.1E} V')
            # st.write(CURRENT_REPORT)
        
        # st.text('')
        # st.text("MEASUREMENT UNITS")
        with st.expander('MEASUREMENT UNITS', icon=':material/square_foot:'): # , border=True
            st.text('')
            units: list = [unit.name for unit in UNITS if unit.value.factor == 1]
            # units.insert(0, '')
            for field in REPORT.MEASUREMENT_UNITS.fields:
                # st.text_input(field.name)
                value = CURRENT_DB[table_db.PROCEDURES.REPORT.name]['MEASUREMENT_UNITS'][field.name]
                indx = None
                if value:
                    indx = units.index(CURRENT_DB[table_db.PROCEDURES.REPORT.name]['MEASUREMENT_UNITS'][field.name])
                globals()[f'unit_{field.name}'] = st.selectbox(field.name, options=units, index=indx)

        # st.line_chart()
        # st.json(CURRENT_DB)

        st.text('')
        if st.button('🔄 UPDATE', use_container_width=True):
            st.write(tx_title)
            st.write(result_type)
            st.write(abs_values)
            st.text('MEASUREMENT_UNITS:')
            for field in REPORT.MEASUREMENT_UNITS.fields:
                st.write(globals()[f'unit_{field.name}'])
            




    ## TEST
    ## __________________________________________________________________________________________________

    with tab_scope:
        CMC_DF = pd.DataFrame(CURRENT_DB[table_db.PROCEDURES.CMC.name])
        TBL_CMC, BTN_UPDATE = TBL_EDITOR(CMC_DF)

        if BTN_UPDATE:
            if len(TBL_CMC) == 0:
                CURRENT_DB[table_db.PROCEDURES.CMC.name] = {}
            else:
                CURRENT_DB[table_db.PROCEDURES.CMC.name] = TBL_CMC.to_dict()
            # SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
            sql_update_db('PROCEDURES', PROCEDURE_ID, CURRENT_DB)
            st.toast("🏁 CMC Updated")



    ## PYDATA
    ## __________________________________________________________________________________________________

    with tab_pydata:
        if not CURRENT_PROCEDURE["PYDATA"]:
            CURRENT_PROCEDURE["PYDATA"] = str()
        PYDATA_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.PYDATA.name])
    


    ## DATA
    ## __________________________________________________________________________________________________
