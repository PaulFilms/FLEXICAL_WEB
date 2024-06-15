'''
FLEXICAL DEVELOPER | MODELS

'''

## PYTHON LIBRARIES
import os, json
from time import sleep
from typing import TypedDict
from dataclasses import dataclass, asdict
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import SSTATE, USUAL_ICONS, GET_FIRM, path_resources, SIDEBAR
from db import conn, execute_query, SQL_SELECT_COLUMN, SQL_ID_COUNT, SQL_INSERT, SQL_MODELS, SQL_PROCEDURES


## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None

if SSTATE.MODELS_COUNT not in st.session_state:
    st.session_state[SSTATE.MODELS_COUNT] = 1

if 'MODEL_COUNT' not in st.session_state:
    st.session_state.MODEL_COUNT = 0

if 'DB_DATA' not in st.session_state:
    st.session_state.DB_DATA = None


## OBJECTS
## __________________________________________________________________________________________________

class MODEL:

    class TypeDict(TypedDict):
        Id: str
        MODEL: str
        MANUFACTURER: str
        DEVICE_TYPE: str
        DESCRIPTION: str
        INFO: str
        DB: dict
        FIRM: str
    
    @dataclass
    class DB:
        RANGE: dict = None
        PART_NUMBER: str = ""
        SPECIFICATIONS: dict = None

        def toJSON(self) -> str:
            return json.dumps(asdict(self))

tbl_specification_config={
        'RANGE1_MIN': st.column_config.NumberColumn(default=0.0),
        'RANGE1_MAX': st.column_config.NumberColumn(default=0.0),
        'RANGE2_MIN': st.column_config.NumberColumn(default=None),
        'RANGE2_MAX': st.column_config.NumberColumn(default=None),
        'EVALUATION': st.column_config.TextColumn(default="-"),
        'RESOLUTION': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C1': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C2': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C3': st.column_config.NumberColumn(format="%.2e", default=0.0),
    }



## MENU
## __________________________________________________________________________________________________

@st.experimental_dialog("NEW MODEL FORM")
def FORM_NEWMODEL():
    DEVICE_TYPE = st.selectbox("TYPE OF DEVICE *", options=SQL_SELECT_COLUMN('DEVICE_TYPES', 'Id'), index=None)
    MANUFACTURER = st.selectbox("MANUFACTURER *", options=SQL_SELECT_COLUMN('MANUFACTURERS', 'Id'), index=None)
    MODEL_ = st.text_input("MODEL *")
    DESCRIPTION = st.text_input("DESCRIPTION")
    INFO = st.text_area("INFO")

    if st.button(label="💽 CREATE NEW MODEL", use_container_width=True):
        CHECK: bool = True
        if CHECK and (not MANUFACTURER or not DEVICE_TYPE or not MODEL_):
            st.warning(f"Complete all * fields", icon=USUAL_ICONS.WARNINNG.value)
            CHECK = False
        sql = execute_query(conn.table("MANUFACTURERS").select("DIMINUTIVE").eq("Id", MANUFACTURER), ttl='10m')
        ID = f"{sql.data[0]['DIMINUTIVE']}_{MODEL_}".replace(chr(32), str())
        if SQL_ID_COUNT("MODELS", ID):
            st.warning(f"< {ID} > is already in the DATABASE", icon=USUAL_ICONS.WARNINNG.value)
            CHECK = False
        if CHECK:
            ## INSERT
            DB = MODEL.DB(RANGE={}, PART_NUMBER="", SPECIFICATIONS={})
            VALUES = {
                "Id": ID.upper(), 
                "MODEL": MODEL_.upper(),
                'MANUFACTURER': MANUFACTURER,
                'DEVICE_TYPE': DEVICE_TYPE,
                'DESCRIPTION': DESCRIPTION.upper(),
                'INFO': INFO,
                'DB': DB.toJSON(),
                "FIRM": GET_FIRM()
            }
            SQL_INSERT("MODELS", VALUES)
            st.session_state[SSTATE.MODELS_COUNT] += 1
            st.info("New Model Added !!", icon='🏁')
            sleep(3)
            st.rerun()

@st.cache_resource
def SQL_MODEL(MODEL_ID: str, COUNT: int):
    print(f"SQL MODEL DATA ({COUNT}):", GET_FIRM())
    return execute_query(conn.table('MODELS').select('*', count='exact').like("Id", MODEL_ID))

def INSERT_PROCEDURE(MODEL_ID: str, DB: dict):
    # print("INSERT_PROCEDURE")
    # for field in DB:
    #     print(DB[field])
    execute_query(conn.table("MODELS").update({"DB": json.dumps(DB)}).eq("Id", MODEL_ID), ttl=0)
    st.session_state.MODEL_COUNT += 1

def get_selected(DATAFRAME: pd.DataFrame, COLUMN: str) -> tuple[pd.DataFrame, str]:
    df_with_selections = DATAFRAME.copy()
    df_with_selections.insert(0, "✔️", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            "✔️": st.column_config.CheckboxColumn(required=True, width='small'),
            'PROCEDURE_ID': st.column_config.TextColumn(required=True, width='large'),
        },
        disabled=DATAFRAME.columns,
        use_container_width=True
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df["✔️"]]
    selected_rows.drop("✔️", axis=1)

    PROCEDURE: str = None
    if len(selected_rows) == 1:
        PROCEDURE = selected_rows['PROCEDURE_ID'].iloc[0]

    return edited_df, PROCEDURE

def FUNC(CURRENT_PROCEDURE: str):

    if CURRENT_PROCEDURE:
        DF = pd.DataFrame(st.session_state.DB_DATA['SPECIFICATIONS'].get(CURRENT_PROCEDURE), columns=list(tbl_specification_config.keys()))
        DF['EVALUATION'] = DF['EVALUATION'].astype(str)
        DF = DF.reset_index()
        del DF['index']

        st.text("") # SEPARATOR
        st.text("") # SEPARATOR
        TBL_DATA = st.data_editor(
            DF,
            hide_index=True,
            num_rows='dynamic',
            column_config=tbl_specification_config,
            use_container_width=True
        )

        if st.button("UPDATE DATA DB"):
            if len(TBL_DATA) == 0:
                st.session_state.DB_DATA['SPECIFICATIONS'][CURRENT_PROCEDURE] = {}
            else:
                st.session_state.DB_DATA['SPECIFICATIONS'][CURRENT_PROCEDURE] = TBL_DATA.to_dict()
            INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
            st.rerun()


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
    st.sidebar.page_link(r"pages/MANUFACTURERS.py", label="MANUFACTURERS", icon="🚗")
    # sd_btn_new = st.sidebar.button("💾 NEW MODEL", use_container_width=True)
    st.sidebar.page_link(r"pages/PROCEDURES.py", label=":blue-background[PROCEDURES]", icon="🧬", use_container_width=True)



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"models.svg"), use_column_width=False)
st.divider()

tab_db, tab_editor = st.tabs(["📒 DATABASE", "✏️ EDITOR"])

## DATABASE
## __________________________________________________________________________________________________

with tab_db:

    if st.button("💾 CREATE NEW MODEL", use_container_width=True): # or sd_btn_new:
        FORM_NEWMODEL()


    if st.session_state[SSTATE.LOGIN_STATUS]:

        st.text("") # SEPARATOR
        st.text("") # SEPARATOR
        st.subheader('DATABASE:', divider='blue')

        # st.sidebar.markdown("""
        # [➡️ DATABASE](#database)
        # """, unsafe_allow_html=True)

        placeholder = st.empty()
        if placeholder.button("🧬 LOAD DATABASE", use_container_width=True):
            with placeholder.expander("🧬 DATABASE", expanded=True):
                SQL = SQL_MODELS(st.session_state[SSTATE.MODELS_COUNT])
                DATAFRAME = pd.DataFrame(SQL)
                del DATAFRAME["DB"]
                st.dataframe(
                    # data=pd.DataFrame(SQL),
                    data=DATAFRAME,
                    use_container_width=True,
                    hide_index=True
                )


## EDITOR
## __________________________________________________________________________________________________

with tab_editor:

    col12, col22 = st.columns(2)

    # if 'MODEL_ID' not in st.session_state:
    #     st.session_state.MODEL_ID = str()

    with col12:
        # MODEL_ID = 
        holder = st.empty()
        MODEL_ID = holder.text_input(label="✏️ ENTER MODEL Id", value="")

    with col22:

        # 
        # DATAFRAME = pd.DataFrame(SQL)
        # print(DATAFRAME)

        st.text("")
        with st.popover(USUAL_ICONS.EXPANDER.value):
            SQL = SQL_MODELS(st.session_state[SSTATE.MODELS_COUNT])
            DATAFRAME = pd.DataFrame(SQL)
            DATAFRAME = DATAFRAME[['Id', "DEVICE_TYPE", 'MANUFACTURER', 'MODEL']]
            # print(DATAFRAME)

            FLTR_DEVICE: str = None
            FLTR_MANUFACTURER: str = None
            FLTR_MODEL: str = None

            def get_filter() -> pd.DataFrame:
                df_filtered = DATAFRAME
                if FLTR_DEVICE:
                    df_filtered = df_filtered[df_filtered['DEVICE_TYPE']==FLTR_DEVICE]
                if FLTR_MANUFACTURER:
                    df_filtered = df_filtered[df_filtered['MANUFACTURER']==FLTR_MANUFACTURER]
                if FLTR_MODEL:
                    df_filtered = df_filtered[df_filtered['MODEL']==FLTR_MODEL]
                return df_filtered

            FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=get_filter()['DEVICE_TYPE'].unique().tolist(), index=None)
            FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=sorted(get_filter()['MANUFACTURER'].unique().tolist()), index=None)
            FLTR_MODEL = st.selectbox("MODEL", options=get_filter()['MODEL'].unique().tolist(), index=None)

            if FLTR_MODEL:
                # st.session_state.MODEL_ID = get_filter()['Id'].iloc[0]
                # print(st.session_state.MODEL_ID)
                # MODEL_ID = st.session_state.MODEL_ID
                # st.rerun()
                MODEL_ID = holder.text_input(label="✏️ ENTER MODEL Id", value=get_filter()['Id'].iloc[0], disabled=False)

    if MODEL_ID:
        SQL = SQL_MODEL(MODEL_ID, st.session_state['MODEL_COUNT'])
        # print(SQL)
        if SQL.count != 1:
            st.session_state.DB_DATA = None
            # st.session_state[MODEL_PROCEDURES] = pd.DataFrame([], columns=["PROCEDURE_ID"])
            st.warning(f"< {MODEL_ID} > don't exits", icon="⚠️")
        else:
            CURRENT_MODEL = MODEL.TypeDict(**SQL.data[0])
            CURRENT_DB = CURRENT_MODEL["DB"]

            ## SPECIFICATIONS
            ## __________________________________________________________________________________________________

            st.text("") # SEPARATOR
            st.markdown(''':blue-background[💊 SPECIFICATIONS:]''')

            # print()
            # print(type(CURRENT_DB))
            # print(CURRENT_DB)

            ## DATA
            if isinstance(CURRENT_DB, str):
                try:
                    st.session_state.DB_DATA = json.loads(CURRENT_DB)
                except:
                    st.session_state.DB_DATA = dict()
            
            elif isinstance(CURRENT_DB, dict):
                st.session_state.DB_DATA = CURRENT_DB
            
            else:
                st.session_state.DB_DATA = dict()

            # print()
            # print(type(st.session_state[DB_DATA]))
            # print(st.session_state[DB_DATA])

            if not st.session_state.DB_DATA.get('SPECIFICATIONS'):
                st.session_state.DB_DATA['SPECIFICATIONS'] = dict()
            
            st.session_state.MODEL_PROCEDURES = pd.DataFrame(list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()), columns=["PROCEDURE_ID"])
            # st.session_state[MODEL_PROCEDURES] = pd.DataFrame(list(st.session_state[SPECIFICATIONS].keys()), columns=["PROCEDURE_ID"])

            ## PROCEDURES

            col12, col22 = st.columns(2)

            with col12:
                TBL_PROCEDURES, CURRENT_PROCEDURE = get_selected(st.session_state.MODEL_PROCEDURES, "")

            with col22:
                with st.popover(label=chr(8801)):
                    with st.container(border=True):
                        if SSTATE.PROCEDURES_COUNT not in st.session_state:
                            st.session_state[SSTATE.PROCEDURES_COUNT] = 1
                        procedure_Id = st.selectbox("PROCEDURE Id", options=[proc['Id'] for proc in SQL_PROCEDURES(st.session_state[SSTATE.PROCEDURES_COUNT])])
                        if st.button(label='➕ INSERT PROCEDURE', use_container_width=True):
                            if procedure_Id in list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()):
                                st.warning(f"< {procedure_Id} > It's already in the list", icon="⚠️")
                            else:
                                st.session_state.DB_DATA['SPECIFICATIONS'][procedure_Id] = {}
                                INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                                st.toast("DATA DB UPDATE")
                                sleep(2)
                                st.rerun()

                    if CURRENT_PROCEDURE and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                        @st.experimental_dialog(title="❓")
                        def YESNO(info: str):
                            st.text(info)
                            col12, col22 = st.columns(2)
                            with col12:
                                if st.button("YES", use_container_width=True):
                                    st.session_state.DB_DATA['SPECIFICATIONS'].pop(CURRENT_PROCEDURE)
                                    INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                                    st.rerun()
                            with col22:
                                if st.button("NO", use_container_width=True):
                                    st.rerun()
                        
                        YESNO(f"DO YOU WANT TO DELETE THIS PROCEDURE?\n< {CURRENT_PROCEDURE} >")

            FUNC(CURRENT_PROCEDURE)

            ## DB DATA JSON
            ## __________________________________________________________________________________________________

            st.text("") # SEPARATOR
            st.text("") # SEPARATOR
            st.markdown(''':blue-background[💊 DB DATA:]''')

            col_1_8, col_8_8 = st.columns([7,1])

            with col_1_8:
                with st.container(border=True):
                    # DICT = st.session_state.current_model_db
                    JSON = json.dumps(st.session_state.DB_DATA)
                    st.json(JSON, expanded=False)
            
            with col_8_8:
                with st.popover(label=chr(8801)):
                    with st.container(border=True):
                        FIELD = st.text_input("FIELD")
                        TYPE_FIELD_VALUE = st.selectbox("DATA TYPE", options=["TEXT", "DECIMAL", "CHECK"])
                        VALUE = st.text_input("VALUE")

                        st.text("") 
                        if st.button("INSERT NEW FIELD ⤵️", use_container_width=True):
                            try:
                                match TYPE_FIELD_VALUE:
                                    case "TEXT":
                                        print("VALUE:", str(VALUE))
                                    case "DECIMAL":
                                        print("VALUE:", float(VALUE))
                                    case "CHECK":
                                        print("VALUE:", bool(VALUE))
                                st.balloons()
                            except:
                                st.warning("Write a valid data")
                
                    with st.container(border=True): # "DELETE"
                        st.selectbox("FIELD", options=list(st.session_state.DB_DATA.keys()))
                        st.text("") 
                        if st.button("DELETE FIELD", use_container_width=True):
                            st.balloons()
