import streamlit as st

from enum import Enum
from typing import Callable

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

def INFOBOX(info: str):
    return st.warning(info, icon="🚨")

@st.experimental_dialog(title="❓")
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

path_resources = r'resources'