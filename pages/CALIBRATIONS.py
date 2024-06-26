'''
FLEXICAL v3 | CALIBRATIONS

'''

## PYTHON LIBRARIES

## IMPORTED LIBRARIES
import streamlit as st

## INTERNAL
from app import *
from db import *


## SESSION STATES
## __________________________________________________________________________________________________





## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
SIDEBAR()

with st.container(border=True):
    st.caption("""
        INCOMPLETE!! 
    """)
    st.caption('''
        In the following updates, this page will manage calibrations, projects/campaigns, and everything related to calibrations
    ''')

st.divider()

st.text('✏️ SELECT CALIBRATION Id')

col12, col22 = st.columns(2)

with col12:
    holder_model = st.empty()
    MODEL_ID = holder_model.text_input(label="✏️ ENTER CALIBRATION Id", value="", label_visibility='collapsed')

with col22:
    with st.popover(USUAL_ICONS.EXPANDER.value):
        st.button(USUAL_ICONS.INSERT.value + " NEW CALIBRATION", use_container_width=True)


# st.camera_input("POLLA")