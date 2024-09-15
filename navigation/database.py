import streamlit as st
from menus import *
from db import *

import pandas as pd

st.text("SELECT TABLE")

col12, col22 = st.columns(2)

with col12:
    TABLE = st.selectbox("TABLES", options=[table.name for table in TABLES], label_visibility='collapsed', index=None)

with col22:
    BTN_NEWITEM = None
    if st.session_state.role == ROLES.ADMIN:
        BTN_NEWITEM = st.button("💾 CREATE NEW ITEM", use_container_width=True)
    
if BTN_NEWITEM:
    # if st.button("💾 CREATE NEW ITEM", use_container_width=True):
    if not TABLE:
        INFOBOX("Please!! Select a valid Table")
    else:
        INFOBOX("This form is not available yet")
    #     if st.session_state.TABLE not in dir(FORMS):
    #         INFOBOX("This form is not available yet")
    #     else:
    #         form = getattr(FORMS, st.session_state.TABLE)
    #         form()

if TABLE:
    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    st.subheader('DATA:', divider='blue')

    SQL = sql_table(TABLE, TABLE)
    DATAFRAME = pd.DataFrame(SQL)
    if "DB" in DATAFRAME.columns:
        del DATAFRAME["DB"]
    if "PYDATA" in DATAFRAME.columns:
        del DATAFRAME["PYDATA"]

    with st.popover(":material/menu:", help="TABLE OPTIONS"):
        st.text("EXPORT TO .xlsx")
        st.text("EXPORT TO .pdf")

    st.dataframe(
        data=DATAFRAME,
        use_container_width=True,
        hide_index=True,
        column_config={colum: st.column_config.TextColumn(label=colum, width=None) for colum in list(DATAFRAME.columns)}
    )


