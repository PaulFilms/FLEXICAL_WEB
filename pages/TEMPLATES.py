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
from menu import SSTATE, GET_FIRM, path_resources, SIDEBAR
from db import conn, execute_query


## MENU
## __________________________________________________________________________________________________


## SESSION STATES
## __________________________________________________________________________________________________

if not st.session_state[SSTATE.LOGIN_STATUS]:
    st.switch_page(r"pages/PROFILE.py")

## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()


## PAGE
## __________________________________________________________________________________________________

st.selectbox