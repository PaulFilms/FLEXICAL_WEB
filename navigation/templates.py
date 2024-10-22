import streamlit as st
from menus import *
from db import *

import os, json
from enum import Enum, auto
from typing import TypedDict
import pandas as pd
import numpy as np

from flexical.database import *
from flexical.definitions import *
from pyreports.xlsx import XLSREPORT
from flexical.report import DOCUMENT


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


## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'filter' not in st.session_state:
    st.session_state.filter = None

for table in ['MODELS', 'PROCEDURES', 'TEMPLATES']:
    if table not in st.session_state:
        st.session_state[table] = 1


## TOOLS
## __________________________________________________________________________________________________

def TEST_EDITOR(ID: str, DB: dict) -> None:
    procedures = sql_column("PROCEDURES", "Id", st.session_state.TEMPLATES)

    @st.dialog(title='✏️ EDITOR', width='small')
    def FORM_NEW():
        PROCEDURE_ID = st.selectbox("PROCEDURE Id *", options=procedures, index=None)
        title = str()
        if PROCEDURE_ID:
            title = sql_row("PROCEDURES", "Id", PROCEDURE_ID, st.session_state.TEMPLATES)['TITLE']
        TEST = st.text_input("TEST TITLE *", value=title)
        PARAMETERS = st.text_input("TEST PARAMETERS")
        CONFIG = st.text_input("CONFIG & CONNECTIONS")
        INFO = st.text_area("INFO")
        if st.button("➕ INSERT NEW TEST", key='btn_test_ADD'):
            NEW_TEST = CALIBRATION.TEST.data(TEST, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, CALIBRATION={})
            DB["TEST_LIST"].append(NEW_TEST.toDict())
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    @st.dialog(title='✏️ EDITOR', width='small')
    def FORM_EDIT(TEST: CALIBRATION.TEST.data, loc):
        indx = None
        if TEST.PROCEDURE_ID in procedures:
            indx = procedures.index(TEST.PROCEDURE_ID)
        PROCEDURE_ID = st.selectbox("PROCEDURE Id", options=procedures, index=indx)
        TITLE = st.text_input("TEST TITLE *", value=TEST.TEST)
        PARAMETERS = st.text_input("TEST PARAMETERS", value=TEST.PARAMETERS)
        CONFIG = st.text_input("CONFIG & CONNECTIONS", value=TEST.CONFIG)
        INFO = st.text_area("INFO", value=TEST.INFO)
        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_test_update'):
            EDIT_TEST = CALIBRATION.TEST.data(TITLE, PARAMETERS, CONFIG, INFO, PROCEDURE_ID, TEST.MEASURES)
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
                test = CALIBRATION.TEST.data(**DB["TEST_LIST"][loc])

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
        DF_CALIBRATION = pd.DataFrame(test.MEASURES, columns=[field.name for field in TEMPLATE.MEASURE])
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
            DB["TEST_LIST"][loc]['MEASURES'] = tbl_cal_test.replace(np.nan, None).to_dict()
            try:
                sql_update_db("TEMPLATES", ID, DB)
                # st.session_state.TEMPLATES += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

def PRINT_TEMPLATE(template_id: str):
    sql_template = sql_row('TEMPLATES', 'Id', template_id, st.session_state.TEMPLATES)
    template_db = json.loads(sql_template['DB'])
    model_id = sql_template['MODEL_ID']
    sql_model = sql_row('MODELS', 'Id', model_id, st.session_state.MODELS)
    model_db = json.loads(sql_model['DB'])

    device = DEVICE.data(
        Id=None,
        MODEL_ID=DEVICE.model(
            MODEL_ID = model_id,
            DEVICE_TYPE = sql_model['DEVICE_TYPE'],
            MANUFACTURER = sql_model['MANUFACTURER'],
            MODEL = sql_model['MODEL']
        ).toDict(),
        SERIAL=None,
        INVENTORY=None,
        OWNER=None,
        OPTIONS=None,
    )

    ## REPORT FOLDER
    if not os.path.exists("REPORTS"):
        os.mkdir('REPORTS')
    file_name: str = f"{template_id}.xlsx"
    file_path: str = os.path.join("REPORTS", file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            INFOBOX('PLEASE, CLOSE THE FILE:\n'+file_path)
            return

    ## REPORT
    xls_report = XLSREPORT(file_path, worksheet_name='TEST_REPORT')
    DOCUMENT.PRINT_XLS.set_format(xls_report)
    DOCUMENT.PRINT_XLS.set_header(xls_report, device=device, logo_path=os.path.join(r'resources',r'logo.png'), scale=13)
    # DOCUMENT.PRINT_XLS.print_page3(xls_report)

    for test in template_db['TEST_LIST']:
        TEST = CALIBRATION.TEST.data(**test)

        procedure_id = TEST.PROCEDURE_ID
        procedure_db = sql_db('PROCEDURES', procedure_id, st.session_state.PROCEDURES)
        # standards = sql_procedure['STANDARDS']
        measures_df = pd.DataFrame(TEST.MEASURES)
        specification_df = pd.DataFrame(model_db['SPECIFICATIONS'][procedure_id])
        cmc_df = pd.DataFrame(procedure_db['CMC'])
        report_format = REPORT.data(
            RESULT_TYPE=procedure_db['REPORT']['RESULT_TYPE'],
            ABSOLUTE_VALUES=procedure_db['REPORT']['ABSOLUTE_VALUES'],
            TESTREPORT=REPORT.TESTREPORT.data(**procedure_db['REPORT']['TESTREPORT']),
            MEASUREMENT_UNITS=REPORT.MEASUREMENT_UNITS.data(**procedure_db['REPORT']['MEASUREMENT_UNITS'])
        )

        DOCUMENT.PRINT_XLS.print_test(xls_report, TEST)

        ## MEASURES
        for loc in measures_df.index:
            row_data = dict(measures_df.loc[loc])
            measure_data = dict()
            for field in CALIBRATION.MEASURE.fields:
                if field.name in row_data: measure_data[field.name] = row_data[field.name]
                else: measure_data[field.name] = None
            measure = CALIBRATION.MEASURE.data(**measure_data)
            if not measure.VALIDATION:
                measure.VALIDATION = dict()
            measure.VALIDATION['PROCEDURE_ID'] = procedure_id

            ## CALCULATION
            VALUE1 = measure.VALUE1
            VALUE2 = measure.VALUE2
            if report_format.ABSOLUTE_VALUES:
                VALUE1 = abs(VALUE1)
                VALUE2 = abs(VALUE2)
            measure.CMC = TABLE_DATA.GET_VALUE(cmc_df, VALUE1, VALUE2)
            measure.LIMIT_OF_ERROR = TABLE_DATA.GET_VALUE(specification_df, VALUE1, VALUE2)
            try: measure.VALIDATION['RESOLUTION'] = specification_df[specification_df['RANGE1_MAX']==specification_df['RANGE']]['RESOLUTION'].max()
            except: measure.VALIDATION['RESOLUTION'] = 0.0

            ## PYDATA

            ## PRINT
            DOCUMENT.PRINT_XLS.print_measure(xls_report, measure, report_format)
            xls_report.row_inc()

        ## FIN TEST
        xls_report.row_inc()
        xls_report.save()

    ## FIN REPORT
    xls_report.close()

    holder_print.download_button(
        label="📩 DOWNLOAD .xlsx File",
        data=open(file_path, "rb").read(),
        file_name=file_name,
        mime="calcs/xlsx",
        use_container_width=True
    )
    os.remove(file_path)

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
        df_filtered = dataFrame.copy()
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

col13, col23, col33 = st.columns([2, 1, 1])

with col13:
    holder_template = st.empty()
    TEMPLATE_ID = holder_template.selectbox("TEMPLATE Id", options=DATAFRAME['Id'].to_list(), index=None, label_visibility='collapsed')

with col23:
    btn_filters = st.button(':material/filter: FILTERS', use_container_width=True)

with col33:
    holder_print = st.empty()
    if TEMPLATE_ID:
        if holder_print.button(":material/file_save: GET TEMPLATE .xlsx", use_container_width=True):
            PRINT_TEMPLATE(template_id=TEMPLATE_ID)

if btn_filters:
    FILTERS(DATAFRAME)

if st.session_state.filter:
    TEMPLATE_ID = holder_template.selectbox("TEMPLATE Id", options=DATAFRAME['Id'].to_list(), index=DATAFRAME['Id'].to_list().index(st.session_state.filter), label_visibility='collapsed')
    st.session_state.filter = None


if TEMPLATE_ID:
    SQL = sql_row('TEMPLATES', 'Id', TEMPLATE_ID, st.session_state.TEMPLATES)
    CURRENT_TEMPLATE = TEMPLATE.TypeDict(**SQL)

    ## DB DATA
    # CURRENT_DB: dict = None
    # if isinstance(CURRENT_TEMPLATE["DB"], str):
    #     try:
    #         CURRENT_DB = json.loads(CURRENT_TEMPLATE["DB"])
    #     except:
    #         CURRENT_DB = dict()
    # elif isinstance(CURRENT_TEMPLATE["DB"], dict):
    #     CURRENT_DB = CURRENT_TEMPLATE["DB"]
    # else:
    #     CURRENT_DB = dict()

    CURRENT_DB = set_db(CURRENT_TEMPLATE)
    CURRENT_TEMPLATE['DB'] = CURRENT_DB
    
    # st.json(CURRENT_TEMPLATE)
    # PRINT_TEMPLATE(CURRENT_TEMPLATE)


    ## TABS
    ## __________________________________________________________________________________________________

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

        selected = TEST_EDITOR(TEMPLATE_ID, CURRENT_DB)



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

