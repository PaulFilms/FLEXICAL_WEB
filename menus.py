import streamlit as st
from db import *

from enum import Enum
from typing import Callable
from io import StringIO


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



## _________________________________________________________________________________________________________________

