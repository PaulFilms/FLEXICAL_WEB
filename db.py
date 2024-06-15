'''
FLEXICAL v3 | DB

https://docs.streamlit.io/develop/tutorials/databases/supabase
pip install st-supabase-connection

'''

## PYTHON LIBRARIES
import json
from dataclasses import dataclass, asdict, fields

## IMPORTED LIBRARIES
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

## INTERNAL
from menu import path_resources, SSTATE, GET_FIRM, USUAL_ICONS


## DATACLASSES
## __________________________________________________________________________________________________



## DB CONNECTION
## __________________________________________________________________________________________________

conn = st.connection("supabase", type=SupabaseConnection)



## DB QUERIES
## __________________________________________________________________________________________________

def SQL_ID_COUNT(TABLE: str, ID: str) -> int:
    return execute_query(conn.table(TABLE).select('*', count='exact').like("Id", ID)).count

def SQL_SELECT_COLUMN(TABLE: str, COLUMN: str) -> list:
    SQL = execute_query(conn.table(TABLE).select(COLUMN).order(COLUMN))
    return [data[COLUMN] for data in SQL.data]

def SQL_INSERT(TABLE: str, VALUES: dict) -> None:
    execute_query(conn.table(TABLE).insert([VALUES]), ttl=0)

@st.cache_resource
def SQL_DEVICE_TYPES(COUNT: int):
    print(f"SQL DEVICE TYPES ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("DEVICE_TYPES").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_MANUFACTURERS(COUNT: int):
    print(f"SQL MANUFACTURERS ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("MANUFACTURERS").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_MODELS(COUNT: int) -> list:
    print(f"SQL MODELS ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("MODELS").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_DEVICES(COUNT: int) -> list:
    print(f"SQL DEVICES ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("DEVICES").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_PROCEDURES(COUNT: int) -> list:
    print(f"SQL PROCEDURES ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("PROCEDURES").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_COMPANIES(COUNT: int):
    print(f"SQL DEVICES ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("DEVICES").select('*').order("Id"), ttl="10m")
    return SQL.data

# CUSTOMERS_COUNT: str = "CUSTOMERS_COUNT"
# if CUSTOMERS_COUNT not in st.session_state:
#     st.session_state[CUSTOMERS_COUNT] = 1

@st.cache_resource
def SQL_CUSTOMERS(COUNT: int):
    print(f"SQL CUSTOMERS ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("CUSTOMERS").select('*').order("Id"), ttl="10m")
    return SQL.data

# import sqlite3

# def get_local_db():
#     conn_sqlite = sqlite3.connect("mydatabase.db")
#     cur_sqlite = conn_sqlite.cursor()
#     # create a table in the SQLite database
#     cur_sqlite.execute("""
#         CREATE TABLE MODELS (
#             Id TEXT PRIMARY KEY,
#             MODEL TEXT,
#             MANUFACTURER INTEGER,
#             DEVICE_TYPE TEXT,
#             DESCRIPTION TEXT,
#             INFO TEXT,
#             DB BLOB,
#             FIRM TEXT
#         );
#     """)
#     for e in SQL_MODELS(0):
#         # print(e)
#         SQL = f"""INSERT INTO MODELS ('Id', 'MODEL', 'MANUFACTURER', 'DEVICE_TYPE', 'DESCRIPTION', 'INFO', 'DB', 'FIRM') VALUES ('{e['Id']}', '{e['MODEL']}', '{e['MANUFACTURER']}', '{e['DEVICE_TYPE']}', '{e['DESCRIPTION']}', '{e['INFO']}', '{e['DB']}', '{e['FIRM']}');"""
#         cur_sqlite.execute(SQL)
#     conn_sqlite.commit()
#     cur_sqlite.close()
#     conn_sqlite.close()

# get_local_db()