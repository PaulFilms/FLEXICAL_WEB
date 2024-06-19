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
from menu import *
from db import *


## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

if 'MODELS' not in st.session_state:
    st.session_state.MODELS = 1

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
        'RESOLUTION': st.column_config.NumberColumn(format="%.2e", default=0.0), #, default=0.0), format="%.2e"
        'C1': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C2': st.column_config.NumberColumn(format="%.2e", default=0.0),
        'C3': st.column_config.NumberColumn(format="%.2e", default=None),
    }



## MENU
## __________________________________________________________________________________________________

def INFO(TEXT: str):
    if st.session_state.info_editor:
        with st.container(border=True):
            st.markdown(TEXT)
    else:
        INFOMD = st.text_area("INFO", value=TEXT, label_visibility='collapsed')
        if INFOMD != CURRENT_MODEL["INFO"]:
            if st.button(USUAL_ICONS.UPDATE.value + " UPDATE INFO"):
                execute_query(conn.table("MODELS").update({"INFO": INFOMD}).eq("Id", MODEL_ID), ttl=0)
                st.session_state.MODELS += 1
                st.toast("INFO Updated")

@st.cache_resource
def SQL_MODEL(MODEL_ID: str, COUNT: int):
    print(f"SQL MODEL DATA ({COUNT}):", GET_FIRM())
    return execute_query(conn.table('MODELS').select('*', count='exact').like("Id", MODEL_ID))

# def INSERT_PROCEDURE(MODEL_ID: str, DB: dict):
#     execute_query(conn.table("MODELS").update({"DB": json.dumps(DB)}).eq("Id", MODEL_ID), ttl=0)
#     st.session_state.MODEL += 1

# def get_selected(DATAFRAME: pd.DataFrame, COLUMN: str) -> tuple[pd.DataFrame, str]:
#     df_with_selections = DATAFRAME.copy()
#     df_with_selections.insert(0, "✔️", False)

#     # Get dataframe row-selections from user with st.data_editor
#     edited_df = st.data_editor(
#         df_with_selections,
#         hide_index=True,
#         column_config={
#             "✔️": st.column_config.CheckboxColumn(required=True, width='small'),
#             'PROCEDURE_ID': st.column_config.TextColumn(required=True, width='large'),
#         },
#         disabled=DATAFRAME.columns,
#         use_container_width=True
#     )

#     # Filter the dataframe using the temporary column, then drop the column
#     selected_rows = edited_df[edited_df["✔️"]]
#     selected_rows.drop("✔️", axis=1)

#     PROCEDURE: str = None
#     if len(selected_rows) == 1:
#         PROCEDURE = selected_rows['PROCEDURE_ID'].iloc[0]

#     return edited_df, PROCEDURE

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
        try:
            col13, col23, col33 = st.columns(3)
            with col13:
                VALUE1 = st.number_input("VALUE1", min_value=TBL_DATA['RANGE1_MIN'].min(), max_value=TBL_DATA['RANGE1_MAX'].max(), label_visibility='collapsed', step=0.0001)
            with col23:
                VALUE2 = st.number_input("VALUE2", min_value=TBL_DATA['RANGE2_MIN'].min(), max_value=TBL_DATA['RANGE2_MAX'].max(), label_visibility='collapsed', step=0.0001)
            with col33:
                VALUE = TABLE_DATA.GET_VALUE(TBL_DATA, VALUE1, VALUE2)
                if VALUE:
                    # st.text(f"RESULT: {VALUE:.2E}")
                    html = '''<div style="text-align: right;">'''
                    html += f"RESULT:  {VALUE:.2E}"
                    html += '''</div>'''
                    st.markdown(html, unsafe_allow_html=True)
        except:
            st.warning(USUAL_ICONS.WARNINNG.value)
        
        if st.button("UPDATE DATA DB"):
            if len(TBL_DATA) == 0:
                st.session_state.DB_DATA['SPECIFICATIONS'][CURRENT_PROCEDURE] = {}
            else:
                st.session_state.DB_DATA['SPECIFICATIONS'][CURRENT_PROCEDURE] = TBL_DATA.to_dict()
            # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
            print(st.session_state.DB_DATA['SPECIFICATIONS'][CURRENT_PROCEDURE])
            SQL_UPDATE_DB("MODELS", MODEL_ID, st.session_state.DB_DATA)
            st.rerun()


## PAGE
## __________________________________________________________________________________________________

if not st.session_state.LOGIN_STATUS:
    st.switch_page(r"pages/LOGIN.py")

## SIDEBAR & BASIC COMPONENTS
st.logo(os.path.join(path_resources, r"LOGO2.svg"))
SIDEBAR()

st.text('✏️ SELECT MODEL Id')

col12, col22 = st.columns(2)

with col12:
    holder_model = st.empty()
    MODEL_ID = holder_model.text_input(label="✏️ ENTER MODEL Id", value="", label_visibility='collapsed')

with col22:
    with st.popover(USUAL_ICONS.EXPANDER.value):
        if "MODELS" not in st.session_state:
            st.session_state = 1
        SQL = SQL_MODELS(st.session_state.MODELS)
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
            MODEL_ID = holder_model.text_input(label="✏️ ENTER MODEL Id", value=get_filter()['Id'].iloc[0], disabled=False, label_visibility='collapsed')

if MODEL_ID:
    # if "MODEL" not in st.session_state:
    #     st.session_state.MODEL = 1
    SQL = SQL_MODEL(MODEL_ID, st.session_state.MODELS)
    # print(SQL)
    if SQL.count != 1:
        CURRENT_MODEL = None
        st.session_state.DB_DATA = None
        st.warning(f"< {MODEL_ID} > don't exits", icon="⚠️")
    else:
        CURRENT_MODEL = MODEL.TypeDict(**SQL.data[0])
        CURRENT_DB = CURRENT_MODEL["DB"]

        ## DB DATA
        if isinstance(CURRENT_DB, str):
            try:
                st.session_state.DB_DATA = json.loads(CURRENT_DB)
            except:
                st.session_state.DB_DATA = dict()
        elif isinstance(CURRENT_DB, dict):
            st.session_state.DB_DATA = CURRENT_DB
        else:
            st.session_state.DB_DATA = dict()

        ## INFO
        ## __________________________________________________________________________________________________

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 INFO & DETAILS:]''')

        st.session_state.info_editor = st.toggle("LOCK", value=True)
        INFO(CURRENT_MODEL["INFO"])

        ## SPECIFICATIONS
        ## __________________________________________________________________________________________________

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 SPECIFICATIONS:]''')

        if not st.session_state.DB_DATA.get('SPECIFICATIONS'):
            st.session_state.DB_DATA['SPECIFICATIONS'] = dict()
        

        ## PROCEDURES

        col12, col22 = st.columns(2)

        with col12:
            # st.session_state.MODEL_PROCEDURES = pd.DataFrame(list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()), columns=["PROCEDURE_ID"])
            COLUMN_NAME = "PROCEDURE Id"
            MODEL_PROCEDURES = pd.DataFrame(list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()), columns=[COLUMN_NAME])
            TBL_PROCEDURES, CURRENT_PROCEDURE = DATAFRAME_LIST(MODEL_PROCEDURES, COLUMN_NAME) # st.session_state.MODEL_PROCEDURES

        with col22:
            with st.popover(label=chr(8801)):
                with st.container(border=True):
                    if 'PROCEDURES' not in st.session_state:
                        st.session_state.PROCEDURES = 1
                    procedure_Id = st.selectbox("PROCEDURE Id", options=[proc['Id'] for proc in SQL_PROCEDURES(st.session_state.PROCEDURES)])
                    if st.button(label='➕ INSERT PROCEDURE', use_container_width=True):
                        if procedure_Id in list(st.session_state.DB_DATA['SPECIFICATIONS'].keys()):
                            st.warning(f"< {procedure_Id} > It's already in the list", icon="⚠️")
                        else:
                            st.session_state.DB_DATA['SPECIFICATIONS'][procedure_Id] = {}
                            # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                            SQL_UPDATE_DB("MODELS", MODEL_ID, st.session_state.DB_DATA)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                if CURRENT_PROCEDURE and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                    @st.experimental_dialog(title="❓")
                    def YESNO_int(info: str):
                        st.text(info)
                        col12, col22 = st.columns(2)
                        with col12:
                            if st.button("YES", use_container_width=True):
                                st.session_state.DB_DATA['SPECIFICATIONS'].pop(CURRENT_PROCEDURE)
                                # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
                                SQL_UPDATE_DB("MODELS", MODEL_ID, st.session_state.DB_DATA)
                                st.rerun()
                        with col22:
                            if st.button("NO", use_container_width=True):
                                st.rerun()
                    
                    YESNO_int(f"DO YOU WANT TO DELETE THIS PROCEDURE?\n< {CURRENT_PROCEDURE} >")

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
        
        # with col_8_8:
        #     with st.popover(label=chr(8801)):
        #         NEW_ITEM = st.text_input("FIELD", label_visibility='collapsed')
        #         if st.button("INSERT NEW FIELD ⤵️", use_container_width=True):
        #             print('AÑDIMOS:', NEW_ITEM)
        #             st.session_state.DB_DATA[NEW_ITEM] = None
        #             INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
        #             st.rerun()

        #         ITEM_2EDIT = st.selectbox("FIELD", options=list(st.session_state.DB_DATA.keys()), label_visibility='collapsed')
        #         @st.experimental_dialog(title="❓")
        #         def EDIT_DATA():
        #             NEW_DATA = st.text_area("JSON")
        #             if st.button("CHECK", use_container_width=True):
        #                 try:
        #                     DATA = {ITEM_2EDIT: eval(NEW_DATA)}
        #                     st.json(json.dumps(DATA))

        #                 except:
        #                     st.warning("Value not valid")
        #             if st.button("CONFIRM", use_container_width=True):
        #                 print(eval(NEW_DATA))
        #                 st.rerun()


        #         if st.button("EDIT FIELD", use_container_width=True):
        #             EDIT_DATA()
        #         on = st.toggle(f"🔒", value=True)

        #         if st.button(f"{USUAL_ICONS.DELETE.value}DELETE FIELD", use_container_width=True, type='primary', disabled=on):
        #             print('BORRAMOS:', ITEM_2EDIT)
        #             # st.session_state.DB_DATA.pop(ITEM_2EDIT)
        #             # INSERT_PROCEDURE(MODEL_ID, st.session_state.DB_DATA)
        #             st.rerun()
        #         # YESNOBOX(f"DO YOU WANT TO DELETE THIS ITEM?\n-> {FIELD_2DEL}", foo)

