import streamlit as st
from db import *

from enum import Enum
from typing import Callable


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


## _________________________________________________________________________________________________________________

