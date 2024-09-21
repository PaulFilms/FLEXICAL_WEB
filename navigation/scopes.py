import streamlit as st
from menus import *
from db import *

from flexical.database import tables



## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if not 'CMC' in st.session_state:
    st.session_state.CMC = 1


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


    ##
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