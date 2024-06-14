'''
FLEXICAL v3 | PROFILE

'''

## PYTHON LIBRARIES
pass

## IMPORTED LIBRARIES
import streamlit as st

## INTERNAL
from menu import SSTATE, SIDEBAR



## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None



## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")



## PAGE
## __________________________________________________________________________________________________

col13, col23, col33 = st.columns(3)

with col33:
    if st.button(f"🌐 {st.session_state[SSTATE.LOGIN_STATUS]}  [Log out]", use_container_width=True):
        st.session_state[SSTATE.LOGIN_STATUS] = None

with st.container(border=True):
    st.caption("This is your Profile page.")
    st.caption("In the next upddates, will you check your data")