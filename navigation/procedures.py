import streamlit as st
from menus import *

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


## TOOLS
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

st.text('SELECT PROCEDURE Id:')

col12, col22 = st.columns(2)

with col12:
    SQL = sql_column('PROCEDURES', tables.CMC.Id.name, st.session_state.PROCEDURES)
    PROCEDURE_ID = st.selectbox("🎛️ PROCEDURE Id", options=[value for value in SQL], index=None, label_visibility='collapsed')

if PROCEDURE_ID:

    CURRENT_PROCEDURE = sql_row('PROCEDURES', 'Id', PROCEDURE_ID, st.session_state.PROCEDURES)
    st.json(CURRENT_PROCEDURE, expanded=False)
    
    
    ## DB DATA
    ## __________________________________________________________________________________________________

    CURRENT_DB: dict = None

    # try:
    CURRENT_DB = CURRENT_PROCEDURE[tables.PROCEDURES.DB.name]
    # excel:
        # CURRENT_DB = dict()
    
    for fld in table_db.PROCEDURES:
        if fld.name not in CURRENT_DB:
            CURRENT_DB[fld.name] = None
    
    fld_report = table_db.PROCEDURES.REPORT.name
    if CURRENT_DB[fld_report] == None: CURRENT_DB[fld_report] = {}
    for fld in REPORT.fields:
        if fld.name not in CURRENT_DB[fld_report]:
            CURRENT_DB[fld_report][fld.name] = None
    
    fld_testreport = REPORT.fields.TESTREPORT.name
    if CURRENT_DB[fld_report][fld_testreport] == None: CURRENT_DB[fld_report][fld_testreport] = {}
    for fld in REPORT.TESTREPORT.fields:
        if fld.name not in CURRENT_DB[fld_report][fld_testreport]:
            CURRENT_DB[fld_report][fld_testreport][fld.name] = None
    
    fld_measurement = REPORT.fields.MEASUREMENT_UNITS.name
    if CURRENT_DB[fld_report][fld_measurement] == None: CURRENT_DB[fld_report][fld_measurement] = {}
    for fld in REPORT.MEASUREMENT_UNITS.fields:
        if fld.name not in CURRENT_DB[fld_report][fld_measurement]:
            CURRENT_DB[fld_report][fld_measurement][fld.name] = None


    ## TABS
    ## __________________________________________________________________________________________________

    st.text('')
    tab_info, tab_testlist, tab_standards, tab_scope, tab_pydata = st.tabs([':material/info: INFO', ':material/lists: TEST', ':material/microwave: STANDARDS', ':material/arrow_range: SCOPE *CMC', ':material/developer_mode: PYDATA'])


    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.INFO.name])

    
    ## TEST
    ## __________________________________________________________________________________________________

    with tab_testlist:
        
        ## TILTE
        st.text('')
        tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE[tables.PROCEDURES.TITLE.name])
        
        ## RESULT_TYPE
        st.text('')
        result_types = [result.name for result in RESULTS.TYPES]
        indx = CURRENT_DB[table_db.PROCEDURES.REPORT.name].get('RESULT_TYPE')
        if indx:
            indx = result_types.index(indx)
        result_type = st.selectbox(
                'TYPE OF RESULT', 
                options=result_types, 
                label_visibility='visible', 
                index=indx
            )
        
        ## ABSOLUTE VALUES
        abs_values = st.toggle('ABSOLUTE VALUES', value=CURRENT_DB[fld_report]['ABSOLUTE_VALUES'])

        ## TEST REPORT
        st.text('')
        st.text('')
        with st.expander('TEST REPORT', icon=':material/lab_profile:'):
            st.text('')
            TESTREPORT = REPORT.TESTREPORT.data(**CURRENT_DB[fld_report][REPORT.fields.TESTREPORT.name])
            # tr_PARAMETERS = st.text_input(REPORT.TESTREPORT.fields.PARAMETERS.name, value=TESTREPORT.PARAMETERS, placeholder='RANGE: {RANGE} V | NOMINAL: {VALUE1} V')
            # tr_MEASUREMENT = st.text_input(REPORT.TESTREPORT.fields.MEASUREMENT.name, value=TESTREPORT.MEASUREMENT, placeholder='{DEVIATION} V')
            # tr_UNCERTAINTY = st.text_input(REPORT.TESTREPORT.fields.UNCERTAINTY.name, value=TESTREPORT.UNCERTAINTY, placeholder='{UNCERTAINTY:.1E} V')
            # tr_LIMIT_OF_ERROR = st.text_input(REPORT.TESTREPORT.fields.LIMIT_OF_ERROR.name, value=TESTREPORT.LIMIT_OF_ERROR, placeholder='± {SPECIFICATION:.1E} V')
            TESTREPORT_DICT = {
                REPORT.TESTREPORT.fields.PARAMETERS.name: st.text_input(REPORT.TESTREPORT.fields.PARAMETERS.name, help='** Example: RANGE: {RANGE} V | NOMINAL: {VALUE1} V', value=TESTREPORT.PARAMETERS, placeholder='RANGE: {RANGE} V | NOMINAL: {VALUE1} V'),
                REPORT.TESTREPORT.fields.MEASUREMENT.name: st.text_input(REPORT.TESTREPORT.fields.MEASUREMENT.name, help='** Example: {DEVIATION} dB', value=TESTREPORT.MEASUREMENT, placeholder='{DEVIATION} V'),
                REPORT.TESTREPORT.fields.UNCERTAINTY.name: st.text_input(REPORT.TESTREPORT.fields.UNCERTAINTY.name, help='** Example: {UNCERTAINTY:.1E} dB', value=TESTREPORT.UNCERTAINTY, placeholder='{UNCERTAINTY:.1E} V'),
                REPORT.TESTREPORT.fields.LIMIT_OF_ERROR.name: st.text_input(REPORT.TESTREPORT.fields.LIMIT_OF_ERROR.name, help='** Example: ± {LIMIT_OF_ERROR:.1E} V', value=TESTREPORT.LIMIT_OF_ERROR, placeholder='± {LIMIT_OF_ERROR:.1E} V'),
            }

        ## MEASUREMENT UNITS
        with st.expander('MEASUREMENT UNITS', icon=':material/square_foot:'): # , border=True
            st.text('')
            units: list = [unit.name for unit in UNITS if unit.value.factor == 1]
            MEASUREMENT_DICT = dict()
            for field in REPORT.MEASUREMENT_UNITS.fields:
                # st.text_input(field.name)
                value = CURRENT_DB[fld_report]['MEASUREMENT_UNITS'][field.name]
                indx = None
                if value:
                    indx = units.index(CURRENT_DB[fld_report]['MEASUREMENT_UNITS'][field.name])
                # globals()[f'unit_{field.name}'] = st.selectbox(field.name, options=units, index=indx)
                MEASUREMENT_DICT[field.name] = st.selectbox(field.name, options=units, index=indx)

        ## UPDATE
        st.text('')
        if st.button('🔄 UPDATE', use_container_width=True):
            CURRENT_DB[fld_report][REPORT.fields.RESULT_TYPE.name] = result_type
            CURRENT_DB[fld_report][REPORT.fields.ABSOLUTE_VALUES.name] = abs_values
            CURRENT_DB[fld_report][fld_testreport] = TESTREPORT_DICT
            CURRENT_DB[fld_report][fld_measurement] = MEASUREMENT_DICT
            supabase.table('PROCEDURES').update({
                    tables.PROCEDURES.TITLE.name: tx_title,
                    # tables.PROCEDURES.DB.name: json.dumps(CURRENT_DB),
                    tables.PROCEDURES.DB.name: CURRENT_DB,
                    tables.PROCEDURES.FIRM.name: get_firm(),
                }).eq('Id', PROCEDURE_ID).execute()
            st.session_state.PROCEDURES += 1
            st.toast("🏁 CMC Updated")

            st.json(CURRENT_DB, expanded=False)


    ## STANDARDS
    ## __________________________________________________________________________________________________

    with tab_standards:
        st.write(CURRENT_DB[table_db.PROCEDURES.STANDARDS.name])


    ## SCOPE CMC
    ## __________________________________________________________________________________________________

    with tab_scope:
        CMC_DF = pd.DataFrame(
            CURRENT_DB[table_db.PROCEDURES.CMC.name],
            columns=list(tbl_cmc_config.keys())
        )
        TBL_CMC, BTN_UPDATE = TBL_EDITOR(CMC_DF)

        if BTN_UPDATE:
            if len(TBL_CMC) == 0:
                CURRENT_DB[table_db.PROCEDURES.CMC.name] = {}
            else:
                CURRENT_DB[table_db.PROCEDURES.CMC.name] = TBL_CMC.replace(np.nan, None).to_dict()
            # SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
            sql_update_db('PROCEDURES', PROCEDURE_ID, CURRENT_DB)
            st.toast("🏁 CMC Updated")



    ## PYDATA
    ## __________________________________________________________________________________________________

    with tab_pydata:
        if not CURRENT_PROCEDURE["PYDATA"]:
            CURRENT_PROCEDURE["PYDATA"] = str()
        PYDATA_EDITOR("PROCEDURES", PROCEDURE_ID, CURRENT_PROCEDURE[tables.PROCEDURES.PYDATA.name])
    


    ## __________________________________________________________________________________________________
