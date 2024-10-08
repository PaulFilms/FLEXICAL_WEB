import streamlit as st
from db import *

from enum import Enum
from typing import Callable, Tuple
from io import StringIO

import pandas as pd
import numpy as np

from flexical.calibration import TABLE_DATA


## _________________________________________________________________________________________________________________

class USUAL_ICONS(Enum): # 🪪 🧮
    HOME = "🏠"
    EXIT = "⛔"
    SAVE = "💾"
    DELETE = "🗑️"
    INSERT = "➕"
    UPDATE = "🔄"
    CHECK = "✅" # ✔️ ✅
    WARNINNG = "🚨" # 🚨 🚩 ⚠️
    UP = "🔼"
    DOWN = "🔽"
    QUESTION = "❓"
    EXPANDER = chr(8801) # ≡
    LOCK = "🔒"
    LOGIN = "🪪"
    PRINT = "🖨️"
    SURE = "🤔"

class ROLES(Enum):
    ADMIN = 'ADMIN'
    TECHNICIAN = 'TECHNICIAN'
    
    @classmethod
    def list(self):
        return [field.name for field in self]

path_resources = r'resources'



## _________________________________________________________________________________________________________________

def INFOBOX(info: str):
    return st.warning(info, icon="🚨")

@st.dialog(title="❓")
def YESNOBOX(info: str, Function: Callable):
    st.text(info)
    col12, col22 = st.columns(2)
    with col12:
        if st.button("YES", use_container_width=True):
            Function()
            st.rerun()
    with col22:
        if st.button("NO", use_container_width=True):
            st.rerun()

def col_sci(label: str):
    return st.column_config.NumberColumn(label=label, format="%.2e")

def MD_EDITOR(table: str, id: str, info: str) -> None:
    '''
    Markdown Editor
    '''
    col12, col22 = st.columns([9,1])
    with col12:
        with st.container(border=True):
            st.markdown(body=info)
    with col22:
        with st.popover(label=USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button(label='✏️ EDITOR', use_container_width=True, key='INFO_EDITOR')
    
    @st.dialog(title='✏️ EDITOR', width='large')
    def EDITOR():
        NEW_INFO = st.text_area(label="tx_markdown_raw", value=info, height=400, label_visibility='collapsed')
        if st.button(label="🔄 UPDATE"):
            try:
                sql_update_id(table, id, {"INFO": NEW_INFO})
                st.session_state[table] += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)
    
    if btn_editor:
        EDITOR()

def PYDATA_EDITOR(TABLE: str, ID: str, PYDATA: str):
    '''
    Python code Editor
    '''
    col12, col22 = st.columns([9,1])
    with col12:
        st.code(PYDATA, language='python')
    with col22:
        with st.popover(USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button('✏️ EDITOR', use_container_width=True, key='PYDATA_EDITOR_EDITOR')
            st.download_button(
                    label=USUAL_ICONS.SAVE.value + " EXPORT .py",
                    data=PYDATA,
                    file_name=f"{ID}.py",
                    mime="application/python",
                    use_container_width=True
                )

    @st.dialog('✏️ EDITOR', width='large')
    def EDITOR():
        new_data = PYDATA
        ## FROM .PY
        uploaded_file = st.file_uploader("CHOOSE A PYTHON FILE:", accept_multiple_files=False, type='py', key="file_uploader")
        if uploaded_file is not None:
            ## To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            new_data = string_data
        NEW_INFO = st.text_area("TEXT EDITOR:", new_data, height=400)
        if st.button("🔄 UPDATE", key="PYDATA_EDITOR_UPDATE"):
            print("UPDATE PYDATA")
            try:
                sql_update_id(TABLE, ID, {"PYDATA": NEW_INFO})
                st.session_state[TABLE] += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    if btn_editor: 
        EDITOR()

def DB_EDITOR(TABLE: str, ID: str, DB: dict):
    col12, col22 = st.columns([9,1])
    with col12:
        with st.container(border=True):
            st.json(DB, expanded=False)
    with col22:
        with st.popover(USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button('✏️ EDITOR', use_container_width=True, key='DB_EDITOR')

    @st.experimental_dialog('✏️ EDITOR', width='large')
    def EDITOR():
        col12, col22 = st.columns(2)
        with col12:
            NEW_ITEM = st.text_input("NEW ITEM", label_visibility='collapsed')
        with col22:
            btn_newitem = st.button("INSERT NEW ITEM")
        if btn_newitem:
            if NEW_ITEM in DB:
                INFOBOX("THIS ITEM IS ALREADY IN THE DB")
            else:
                DB[NEW_ITEM] = None
        
        st.divider()
        st.text("SELECT ITEM")
        col12, col22 = st.columns(2)
        with col12:
            ITEM = st.selectbox("EDIT ITEM", options=list(DB.keys()), label_visibility='collapsed')
        with col22:
            btn_deleteitem = st.button("DELETE ITEM")
        if ITEM and btn_deleteitem:
            del DB[ITEM]
            sql_update_db(TABLE, ID, DB)
            st.rerun()
        if ITEM:
            TEXT = st.text_area("CONTENT", DB[ITEM])
            VALUE = None
            col12, col22 = st.columns(2)
            with col12:
                VALIDATION = st.selectbox("VALIDATION", options=["BOOL", "TEXT", "NUMBER", "JSON"], label_visibility='collapsed')
            with col22:
                btn_validate = st.button("VALIDATE")
            holder_update = st.empty()

            def VALIDATE():
                try:
                    match VALIDATION:
                        case "BOOL": VALUE = bool(TEXT)
                        case "TEXT": VALUE = str(TEXT)
                        case "NUMBER": VALUE = float(TEXT)
                        case "JSON": 
                            VALUE = TEXT.replace(chr(39), chr(34))
                            VALUE = VALUE.replace("None", "null")
                            VALUE = VALUE.replace("nan", "null")
                            VALUE = dict(json.loads(VALUE))
                            # VALUE = json.dumps(VALUE)
                    st.success(VALUE)
                    holder_update.button("UPDATE")
                except Exception as e:
                    INFOBOX(e)
                    VALUE = None
                return VALUE

            if btn_validate:
                VALIDATE()

            # btn_update = st.button("🔄 UPDATE")
            # if btn_update:
            #     NEW_VALUE = VALIDATE()
            #     print("UPDATE", NEW_VALUE)
            #     st.rerun()

            # if btn_update:
            #     DB[ITEM] = VALUE
            #     print("UPDATE", DB)
            #     SQL_UPDATE_DB(TABLE, ID, DB)
            #     st.rerun()
            if holder_update:
                print("UPDATE")
                st.rerun()

    
    if btn_editor: EDITOR()

def TBL_EDITOR(DATAFRAME: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
    '''
    Render a st.data_editor with the basics fields to use for calculation
    RANGE1, RANGE2, EVALUATION, C1, C2, C3 ...
    '''
    with st.popover(USUAL_ICONS.EXPANDER.value):
        tg_format = st.toggle('FORMAT DECIMAL', value=False)
        tg_checker = st.toggle('CHECKER', value=False)

    if "tbl_float_format" not in st.session_state:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format="%.2e")
    
    if tg_format:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format=None)
    else:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format="%.2e")

    DATAFRAME['RANGE1_MIN'] = DATAFRAME['RANGE1_MIN'].astype(float)
    DATAFRAME['RANGE1_MAX'] = DATAFRAME['RANGE1_MAX'].astype(float)
    DATAFRAME['RANGE2_MIN'] = DATAFRAME['RANGE2_MIN'].astype(float)
    DATAFRAME['RANGE2_MAX'] = DATAFRAME['RANGE2_MAX'].astype(float)
    DATAFRAME['C1'] = DATAFRAME['C1'].astype(float)
    DATAFRAME['C2'] = DATAFRAME['C2'].astype(float)
    DATAFRAME['C3'] = DATAFRAME['C3'].astype(float)
    DATAFRAME['EVALUATION'] = DATAFRAME['EVALUATION'].astype(str)
    DATAFRAME.insert(len(DATAFRAME.columns)-1, 'EVALUATION', DATAFRAME.pop('EVALUATION'))
    DATAFRAME = DATAFRAME.reset_index()
    del DATAFRAME['index']

    column_config = dict()
    for column in list(DATAFRAME.columns):
        if DATAFRAME[column].dtype == np.float64:
            # print("FLOAT")
            column_config[column] = st.session_state.tbl_float_format
    column_config['EVALUATION'] = st.column_config.TextColumn(default="(VALUE1*C1*1e1) + (C2*1e1) # VALUE1(<unit>), VALUE2(null)")

    TABLE_EDITOR = st.data_editor(
        DATAFRAME,
        hide_index=True,
        num_rows='dynamic',
        # column_config={
        #     'RANGE1_MIN': st.session_state.tbl_float_format,
        #     'RANGE1_MAX': st.session_state.tbl_float_format,
        #     'RANGE2_MIN': st.session_state.tbl_float_format,
        #     'RANGE2_MAX': st.session_state.tbl_float_format,
        #     'C1': st.session_state.tbl_float_format,
        #     'C2': st.session_state.tbl_float_format,
        #     'C3': st.session_state.tbl_float_format,
        #     'EVALUATION': st.column_config.TextColumn(default="(VALUE1*C1*1e1) + (C2*1e1) # VALUE2"),
        # },
        column_config=column_config,
        use_container_width=True
    )

    if tg_checker:
        with st.container(border=False):
            col13, col23, col33 = st.columns([1,1,2])
            with col13:
                VALUE1 = st.number_input("VALUE1", label_visibility='collapsed', min_value=TABLE_EDITOR['RANGE1_MIN'].min(), max_value=TABLE_EDITOR['RANGE1_MAX'].max())
            with col23:
                VALUE2 = st.number_input("VALUE2", label_visibility='collapsed', min_value=TABLE_EDITOR['RANGE2_MIN'].min(), max_value=TABLE_EDITOR['RANGE2_MAX'].max())
            with col33:
                result = str()
                if VALUE1: result += f'VALUE1: {VALUE1} | '
                if VALUE2 and not pd.isnull(VALUE2): result += f'VALUE2: {VALUE2} | '
                RESULT = TABLE_DATA.GET_VALUE(TABLE_EDITOR, VALUE1, VALUE2)
                if RESULT:  result += f'RESULT: {RESULT:.2E}'
                else: result += f'RESULT: --'
                st.text(result)
    
    btn_update = st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key="TBL_EDITOR")
    
    return TABLE_EDITOR, btn_update


## _________________________________________________________________________________________________________________

