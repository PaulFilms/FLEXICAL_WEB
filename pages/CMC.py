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

if not 'PROCEDURES' in st.session_state:
    st.session_state.PROCEDURES = 1


## MENU
## __________________________________________________________________________________________________

class SERIE(TypedDict):
    Id: str
    INFO: str
    DB: dict

## PAGE
## __________________________________________________________________________________________________

SIDEBAR()

st.text('MODEL SERIES Id')

col12, col22 = st.columns(2)

SQL = execute_query(conn.table("CMC").select('*').order('Id')).data
print("SQL:\n", SQL)

with col12:
    SERIE_ID = st.selectbox("SERIE Id", options=[id_serie['Id'] for id_serie in SQL], index=None, label_visibility='collapsed')


if SERIE_ID:

    SQL = SQL_BY_ROW("CMC", "Id", SERIE_ID)[0]
    CURRENT_SERIE = SERIE(**SQL)
    
    ## DB DATA
    CURRENT_DB: dict = None
    if isinstance(CURRENT_SERIE["DB"], str):
        try:
            CURRENT_DB = json.loads(CURRENT_SERIE["DB"])
        except:
            CURRENT_DB = dict()
    elif isinstance(CURRENT_SERIE["DB"], dict):
        CURRENT_DB = CURRENT_SERIE["DB"]
    else:
        CURRENT_DB = dict()

    st.json(CURRENT_SERIE, expanded=False)

    ## INFO
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('INFO:', divider='blue')

    INFO_EDITOR("CMC", SERIE_ID, CURRENT_SERIE["INFO"])


    ## MODELS
    ## __________________________________________________________________________________________________

    # st.text("")
    # st.text("")
    st.subheader('STANDARD MODELS:', divider='blue')
    # st.markdown(''':blue-background[💊 MODELS:]''')

    if not CURRENT_DB.get('MODELS'):
        CURRENT_DB['MODELS'] = dict()

    col12, col22 = st.columns(2)

    with col12:
        models = list(CURRENT_DB['MODELS'].keys())
        model = st.dataframe(
            data=pd.DataFrame(models, columns=['VALUE']),
            use_container_width=True,
            hide_index=True,
            on_select="rerun", # Con esta opcion aparece el selector de fila
            selection_mode=['single-row'], # "multi-column" "multi-row"
        )
        if len(model.selection.rows):
            CURRENT_MODEL = models[model.selection.rows[0]]
        else:
            CURRENT_MODEL = None

    column_config={
        "RANGE": st.column_config.NumberColumn(),
        'VALUE1': st.column_config.NumberColumn(),
        'VALUE2': st.column_config.NumberColumn()
    }

    with col22:
        with st.popover(label=chr(8801)):
            with st.container(border=True):
                if 'MODELS' not in st.session_state:
                    st.session_state.MODELS = 1
                model_Id = st.selectbox("MODEL Id", options=[proc['Id'] for proc in SQL_MODELS(st.session_state.MODELS)])
                if st.button(label='➕ INSERT MODEL', use_container_width=True):
                    if model_Id in list(CURRENT_DB['MODELS'].keys()):
                        st.warning(f"< {model_Id} > It's already in the list", icon="⚠️")
                    else:
                        CURRENT_DB['MODELS'][model_Id] = {}
                        # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                        SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
                        st.toast("DATA DB UPDATE")
                        sleep(2)
                        st.rerun()

                if CURRENT_MODEL and st.button("🗑️ DELETE MODEL", use_container_width=True):
                    def DELETE_MODEL():
                        CURRENT_DB['MODELS'].pop(CURRENT_MODEL)
                        SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
                        st.rerun()
                    YESNOBOX(f"DO YOU WANT TO DELETE THIS MODEL?\n< {CURRENT_MODEL} >", DELETE_MODEL)


    ## PROCEDURES
    ## __________________________________________________________________________________________________

    st.text("")
    st.text("")
    st.subheader('PROCEDURES:', divider='blue')
    # st.markdown(''':blue-background[💊 PROCEDURES:]''')

    PROCEDURES = [proc['Id'] for proc in SQL_PROCEDURES(st.session_state.PROCEDURES)]

    col12, col22 = st.columns(2)

    if not CURRENT_DB.get('PROCEDURES'):
        CURRENT_DB['PROCEDURES'] = dict()

    with col12:
        procedures = list(CURRENT_DB['PROCEDURES'].keys())
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
                procedure_Id = st.selectbox("PROCEDURE Id", options=PROCEDURES)
                if st.button(label='➕ INSERT PROCEDURE', use_container_width=True):
                    if procedure_Id in list(CURRENT_DB['PROCEDURES'].keys()):
                        st.warning(f"< {procedure_Id} > It's already in the list", icon="⚠️")
                    else:
                        CURRENT_DB['PROCEDURES'][procedure_Id] = {}
                        # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                        SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
                        st.toast("DATA DB UPDATE")
                        sleep(2)
                        st.rerun()

                if CURRENT_PROCEDURE and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                    def DELETE_PROCEDURE():
                        CURRENT_DB['PROCEDURES'].pop(CURRENT_PROCEDURE)
                        SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
                        st.rerun()
                    YESNOBOX(f"DO YOU WANT TO DELETE THIS PROCEDURE?\n< {CURRENT_PROCEDURE} >", DELETE_PROCEDURE)
                
                if CURRENT_PROCEDURE:
                    if not CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE].get("DUT"):
                        CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT'] = None
                        indx = None
                    else:
                        indx = PROCEDURES.index(CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT'])
                    procedure_dut = st.selectbox("DUT", options=PROCEDURES, index=indx)
                    if st.button(USUAL_ICONS.UPDATE.value + " UPDATE DUT", use_container_width=True):
                        CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT'] = procedure_dut
                        SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
                        st.rerun()

    if CURRENT_PROCEDURE:

        ## CMC
        ## __________________________________________________________________________________________________

        # st.text("")
        # st.text("")
        # st.subheader('MODELS:', divider='blue')
        st.markdown(''':blue-background[💊 CMC:]''')

        # st.write(CURRENT_PROCEDURE)

        if not CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE].get('CMC'):
            CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['CMC'] = dict()

        column_config={
            "RANGE": st.column_config.NumberColumn(),
            'VALUE1': st.column_config.NumberColumn(),
            'VALUE2': st.column_config.NumberColumn(),
            'CMC': COL_SCI("CMC")
        }

        st.write("VDC_METERS")

        ## CMC
        if CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT']:
            SQL_PROCEDURE = SQL_BY_ROW("PROCEDURES", "Id", CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT'])[0]
            if isinstance(SQL_PROCEDURE['DB'], dict): PROCEDURE_DB = SQL_PROCEDURE['DB']
            if isinstance(SQL_PROCEDURE['DB'], str): PROCEDURE_DB = json.loads(SQL_PROCEDURE['DB'])
            if not PROCEDURE_DB.get('CMC') or len(PROCEDURE_DB['CMC']) == 0:
                CMC_DF = None
            else:
                CMC_DF = pd.DataFrame(PROCEDURE_DB['CMC'])
        else:
            CMC_DF = None

        ## MODELS
        MODELS = dict()
        for model in models:
            MODEL_SQL = SQL_BY_ROW("MODELS", "Id", model)[0]
            if isinstance(MODEL_SQL['DB'], dict): MODEL_DB = MODEL_SQL['DB']
            if isinstance(MODEL_SQL['DB'], str): MODEL_DB = json.loads(MODEL_SQL['DB'])
            if not MODEL_DB['SPECIFICATIONS'].get(CURRENT_PROCEDURE) or len(MODEL_DB['SPECIFICATIONS'][CURRENT_PROCEDURE]) == 0:
                MODELS[model] = None
            else:
                MODELS[model] = pd.DataFrame(MODEL_DB['SPECIFICATIONS'][CURRENT_PROCEDURE])
            column_config[model] = COL_SCI(model)

        columns = [field for field in column_config.keys()]
        # columns.append("CMC")
        # columns.extend(model for model in CURRENT_DB['MODELS'])

        DATAFRAME = pd.DataFrame(CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['CMC'], columns=columns)
        DATAFRAME = DATAFRAME.reset_index()
        del DATAFRAME['index']

        ## RECALC
        for iloc in range(len(DATAFRAME)):
            VALUE1 = DATAFRAME.iloc[iloc]['VALUE1']
            VALUE2 = DATAFRAME.iloc[iloc]['VALUE2']
            # print(iloc, VALUE1)
            if isinstance(CMC_DF, pd.DataFrame):
                DATAFRAME.at[iloc, 'CMC'] = TABLE_DATA.GET_VALUE(CMC_DF, VALUE1, VALUE2)
            # print(models)
            for model in models:
                if isinstance(MODELS[model], pd.DataFrame):
                    DATAFRAME.at[iloc, model] = TABLE_DATA.GET_VALUE(MODELS[model], VALUE1, VALUE2)

        TBL_CMC = st.data_editor(
            data=DATAFRAME, 
            use_container_width=True, 
            hide_index=True,
            num_rows='dynamic',
            column_config=column_config
        )

        if st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key="TBL_EDITOR"):
            if len(TBL_CMC) == 0:
                CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['CMC'] = {}
            else:
                CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['CMC'] = TBL_CMC.to_dict()
            SQL_UPDATE_DB("CMC", SERIE_ID, CURRENT_DB)
            st.toast("🏁 CMC Updated")


        ## CMC GRAPHIC
        ## __________________________________________________________________________________________________

        st.text("")
        st.text("")
        st.subheader('CMC (TYPE B):', divider='blue')

        with st.container(border=True):
            col12, col22 = st.columns(2)
            with col12:
                RANGE = st.selectbox("RANGE", options=TBL_CMC['RANGE'].unique().tolist())

            chart_dict_data = {
                "VALUE1": TBL_CMC[TBL_CMC['RANGE']==RANGE]['VALUE1'],
                "CMC": TBL_CMC[TBL_CMC['RANGE']==RANGE]['CMC'],
                # "col3": np.random.choice(["A", "B", "C"], 20),
            }
            for model in MODELS:
                chart_dict_data[model] = TBL_CMC[TBL_CMC['RANGE']==RANGE][model]

            chart_data = pd.DataFrame(chart_dict_data)
            st.line_chart(
                chart_data, 
                x="VALUE1", 
                y=["CMC"]+[model for model in MODELS],
                y_label="ppm"
            )
