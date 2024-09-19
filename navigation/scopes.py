import os
from menus import *
from db import *

if 'role' not in st.session_state:
    st.session_state.role = None

if not 'PROCEDURES' in st.session_state:
    st.session_state.PROCEDURES = 1

st.text('MODEL SERIES Id')

col12, col22 = st.columns(2)

# SQL = execute_query(conn.table("CMC").select('*').order('Id')).data
SQL = sql_table('CMC', st.session_state.PROCEDURES)
st.write(SQL)