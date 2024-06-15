'''
FLEXICAL v3 | PROFILE

'''

## PYTHON LIBRARIES
from time import sleep

## IMPORTED LIBRARIES
import streamlit as st

## INTERNAL
from menu import SSTATE, SIDEBAR, USUAL_ICONS
from db import SQL_MODELS



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

# col13, col23, col33 = st.columns(3)

# with col33:
#     if st.button(f"🌐 {st.session_state[SSTATE.LOGIN_STATUS]}  [Log out]", use_container_width=True):
#         st.session_state[SSTATE.LOGIN_STATUS] = None

with st.container(border=True):
    st.caption("This is your Profile page.")
    st.caption("In the next upddates, will you check your data")

if st.session_state[SSTATE.LOGIN_STATUS]:
    st.divider()
    text_contents = '''This is some text'''
    st.download_button(USUAL_ICONS.SAVE.value + " DOWNLOAD DESKTOP APP", text_contents, use_container_width=True)
    st.download_button(USUAL_ICONS.SAVE.value + " DOWNLOAD DATABASE", text_contents, use_container_width=True)

st.divider()

import pandas as pd

# create a sample dataframe
# if "df" not in st.session_state:
#     st.
st.session_state.df = pd.DataFrame({
    'column1': ['apple', 'banana', 'banana', 'cherry', 'date', 'date', 'date', 'elderberry'],
    'column2': ['red', 'yellow', 'green', 'red', 'yellow', 'green', 'green', 'red'],
    'column3': [1, 2, 2, 3, 4, 4, 4, 5]
})

st.session_state.column1_values = None
st.session_state.column2_values = None
st.session_state.column3_values = None

def filtered() -> pd.DataFrame:
    df_fltr = st.session_state.df
    if st.session_state.column1_values:
        df_fltr = df_fltr[df_fltr['column1']==st.session_state.column1_values]
    if st.session_state.column2_values:
        df_fltr = df_fltr[df_fltr['column2']==st.session_state.column2_values]
    if st.session_state.column3_values:
        df_fltr = df_fltr[df_fltr['column3']==st.session_state.column3_values]
    return df_fltr

# create three selectboxes for each column
# column1_values = sorted(filtered()['column1'].unique().tolist())
# column2_values = sorted(filtered()['column2'].unique().tolist())
# column3_values = sorted(filtered()['column3'].unique().tolist())

st.session_state.column1_values = st.selectbox('Select column1 value:', sorted(filtered()['column1'].unique().tolist()), index=None)
st.session_state.column2_values = st.selectbox('Select column2 value:', sorted(filtered()['column2'].unique().tolist()), index=None)
st.session_state.column3_values = st.selectbox('Select column3 value:', sorted(filtered()['column3'].unique().tolist()), index=None)

# # filter the dataframe based on the selected values
# filtered_df = st.session_state.df.query(
#     f"column1 == '{selected_column1}' and column2 == '{selected_column2}' and column3 == {selected_column3}"
# )

# # display the filtered dataframe
# st.write(st.session_state.df)

st.write(filtered())

import sqlite3

# st.download_button(
#     label="Download SQLite Database",
#     data=lambda: open("mydatabase.db", "rb").read(),
#     file_name="mydatabase.db",
#     mime="application/x-sqlite3",
#     key="download_db"
# )

holder = st.empty()

if holder.button("GET DATABASE"):
    with st.spinner("Generating SQLite database..."):
        conn_sqlite = sqlite3.connect("mydatabase.db")
        cur_sqlite = conn_sqlite.cursor()
        # create a table in the SQLite database
        cur_sqlite.execute("""
            CREATE TABLE MODELS (
                Id TEXT PRIMARY KEY,
                MODEL TEXT,
                MANUFACTURER INTEGER,
                DEVICE_TYPE TEXT,
                DESCRIPTION TEXT,
                INFO TEXT,
                DB BLOB,
                FIRM TEXT
            );
        """)
        for e in SQL_MODELS(0):
            # print(e)
            SQL = f"""INSERT INTO MODELS ('Id', 'MODEL', 'MANUFACTURER', 'DEVICE_TYPE', 'DESCRIPTION', 'INFO', 'DB', 'FIRM') VALUES ('{e['Id']}', '{e['MODEL']}', '{e['MANUFACTURER']}', '{e['DEVICE_TYPE']}', '{e['DESCRIPTION']}', '{e['INFO']}', '{e['DB']}', '{e['FIRM']}');"""
            cur_sqlite.execute(SQL)
        conn_sqlite.commit()
        cur_sqlite.close()
        conn_sqlite.close()
        sleep(2)
    
    holder.download_button(
        label="Download SQLite Database",
        data=open("mydatabase.db", "rb").read(),
        file_name="mydatabase.db",
        mime="application/x-sqlite3"
    )

# create a context manager to generate the SQLite database file
# with st.spinner("Generating SQLite database..."):
#     with open("mydatabase.db", "wb") as f:
#         # create a connection to a new in-memory SQLite database
#         conn = sqlite3.connect(":memory:")

#         # create a cursor for the SQLite database
#         cur = conn.cursor()

#         # create a table in the SQLite database
#         cur.execute("""
#         CREATE TABLE MODELS (
#             Id TEXT PRIMARY KEY,
#             MODEL TEXT,
#             MANUFACTURER INTEGER,
#             DEVICE_TYPE TEXT,
#             DESCRIPTION TEXT,
#             INFO TEXT,
#             DB BLOB,
#             FIRM TEXT
#             );
#         """)

#         # insert some data into the table
#         for e in SQL_MODELS(0):
#             # print(e)
#             SQL = f"""INSERT INTO MODELS ('Id', 'MODEL', 'MANUFACTURER', 'DEVICE_TYPE', 'DESCRIPTION', 'INFO', 'DB', 'FIRM') VALUES ('{e['Id']}', '{e['MODEL']}', '{e['MANUFACTURER']}', '{e['DEVICE_TYPE']}', '{e['DESCRIPTION']}', '{e['INFO']}', '{e['DB']}', '{e['FIRM']}');"""
#             cur.execute(SQL)

#         # commit the changes to the SQLite database
#         conn.commit()

#         # write the SQLite database file to disk
#         f.write(conn.backup("main", "."))

#         # close the database connection
#         cur.close()
#         conn.close()