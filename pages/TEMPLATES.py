'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import *
from db import *


## MENU
## __________________________________________________________________________________________________


## SESSION STATES
## __________________________________________________________________________________________________

# if not st.session_state[SSTATE.LOGIN_STATUS]:
#     st.switch_page(r"pages/PROFILE.py")

## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
# st.sidebar.divider()


## PAGE
## __________________________________________________________________________________________________

st.text('TEMPLATE Id')

col12, col22 = st.columns(2)

with col12:
    st.selectbox("TEMPLATE Id", options=SQL_SELECT_COLUMN("TEMPLATES", "Id"), index=None, label_visibility='collapsed')

with col22:
    with st.popover(USUAL_ICONS.EXPANDER.value):
        FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=SQL_SELECT_COLUMN("DEVICE_TYPES", "Id"), index=None)
        FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=SQL_SELECT_COLUMN("MANUFACTURERS", "Id"), index=None)
        FLTR_MODEL = st.selectbox("MODEL", options=SQL_SELECT_COLUMN("MODELS", "Id"), index=None)


# FOOTER("FLEXICAL | TEMPLATES EDITOR")
