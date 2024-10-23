import streamlit as st
from menus import *
from db import *

from time import sleep

from flexical.database import tables



## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if not 'CMC' in st.session_state:
    st.session_state.CMC = 1

if not 'MODELS' in st.session_state:
    st.session_state.MODELS = 1

if not 'PROCEDURES' in st.session_state:
    st.session_state.PROCEDURES = 1



## PAGE
## __________________________________________________________________________________________________

st.text('MODEL SERIES Id')

col12, col22 = st.columns(2)

# SQL = execute_query(conn.table("CMC").select('*').order('Id')).data
# SQL = sql_table('CMC', st.session_state.PROCEDURES)
# st.write(SQL)

with col12:
    SQL = sql_column('CMC', tables.CMC.Id.name, st.session_state.CMC)
    MODEL_ID = st.selectbox("🎛️ PROCEDURE Id", options=[value for value in SQL], index=None, label_visibility='collapsed')

if MODEL_ID:
    CURRENT_SERIE = sql_row('CMC', 'Id', MODEL_ID, st.session_state.CMC)
    st.json(CURRENT_SERIE, expanded=False)

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

    ## TABS
    ## __________________________________________________________________________________________________

    st.text('')
    tab_info, tab_scope = st.tabs([':material/info: INFO', ':material/arrow_range: SCOPE *CMC']) #, ':material/lists: TEST', ':material/microwave: STANDARDS', ':material/developer_mode: PYDATA'])
    # tab_testlist, tab_standards, , tab_pydata



    ## INFO
    ## __________________________________________________________________________________________________

    with tab_info:
        MD_EDITOR("CMC", MODEL_ID, CURRENT_SERIE[tables.CMC.INFO.name])


    ## SCOPE
    ## __________________________________________________________________________________________________

    with tab_scope:

        ## MODELS
        ## __________________________________________________________________________________________________
        
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
                    models_list = sql_column('MODELS', 'Id', st.session_state.MODELS)
                    model_Id = st.selectbox("MODEL Id", options=[model for model in models_list])
                    if st.button(label='➕ INSERT MODEL', use_container_width=True):
                        if model_Id in list(CURRENT_DB['MODELS'].keys()):
                            st.warning(f"< {model_Id} > It's already in the list", icon="⚠️")
                        else:
                            CURRENT_DB['MODELS'][model_Id] = {}
                            sql_update_db('CMC', MODEL_ID, CURRENT_DB)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                    if CURRENT_MODEL and st.button("🗑️ DELETE MODEL", use_container_width=True):
                        def DELETE_MODEL():
                            CURRENT_DB['MODELS'].pop(CURRENT_MODEL)
                            sql_update_db('CMC', MODEL_ID, CURRENT_DB)
                            st.rerun()
                        YESNOBOX(f"DO YOU WANT TO DELETE THIS MODEL?\n< {CURRENT_MODEL} >", DELETE_MODEL)


        ## PROCEDURES
        ## __________________________________________________________________________________________________

        st.text("")
        st.text("")
        st.subheader('PROCEDURES:', divider='blue')
        # st.markdown(''':blue-background[💊 PROCEDURES:]''')

        # PROCEDURES = [proc['Id'] for proc in SQL_PROCEDURES(st.session_state.PROCEDURES)]
        PROCEDURES = sql_column('PROCEDURES', 'Id', st.session_state.PROCEDURES)

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
                            sql_update_db('CMC', MODEL_ID, CURRENT_DB)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                    if CURRENT_PROCEDURE and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                        def DELETE_PROCEDURE():
                            CURRENT_DB['PROCEDURES'].pop(CURRENT_PROCEDURE)
                            sql_update_db('CMC', MODEL_ID, CURRENT_DB)
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
                            sql_update_db('CMC', MODEL_ID, CURRENT_DB)
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
                'CMC': col_sci("CMC")
            }

            st.write("VDC_METERS")

            ## CMC
            if CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT']:
                SQL_PROCEDURE = sql_row('PROCEDURES', 'Id', CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['DUT'], st.session_state.PROCEDURES)
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
                # MODEL_SQL = SQL_BY_ROW("MODELS", "Id", model)[0]
                MODEL_SQL = sql_row('MODELS', 'Id', model, st.session_state.MODELS)
                if isinstance(MODEL_SQL['DB'], dict): MODEL_DB = MODEL_SQL['DB']
                if isinstance(MODEL_SQL['DB'], str): MODEL_DB = json.loads(MODEL_SQL['DB'])
                if not MODEL_DB['SPECIFICATIONS'].get(CURRENT_PROCEDURE) or len(MODEL_DB['SPECIFICATIONS'][CURRENT_PROCEDURE]) == 0:
                    MODELS[model] = None
                else:
                    MODELS[model] = pd.DataFrame(MODEL_DB['SPECIFICATIONS'][CURRENT_PROCEDURE])
                column_config[model] = col_sci(model)

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
                    CURRENT_DB['PROCEDURES'][CURRENT_PROCEDURE]['CMC'] = TBL_CMC.replace(np.nan, None).to_dict()
                sql_update_db('CMC', MODEL_ID, CURRENT_DB)
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
