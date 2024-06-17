'''
FLEXICAL v3 | DB

`SUPABASE INFO:`
    pip install st-supabase-connection
    https://docs.streamlit.io/develop/tutorials/databases/supabase

'''

## PYTHON LIBRARIES
import os, json, sqlite3
from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import TypedDict
from time import sleep

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

class DB:

    class TABLES(Enum):
        COMPANIES = "COMPANIES"
        DEVICE_TYPES = "DEVICE_TYPES"
        MANUFACTURERS = "MANUFACTURERS"
        MODELS = "MODELS"
        DEVICES = "DEVICES"
        PROCEDURES = "PROCEDURES"
        TEMPLATES = "TEMPLATES"

    class COMPANIES(TypedDict):
        Id: str
        FULL_NAME: str
        COUNTRY: str
        ADDRESS1: str
        ADDRESS2: str
        POST_CODE: str
        WEB_LINK: str
        FIRM: str

    class DEVICE_TYPES(TypedDict):
        Id: str
        DESCRIPTION: str
        FIRM: str

    @dataclass
    class MODEL_DB:
        RANGE: dict = None
        PART_NUMBER: str = ""
        SPECIFICATIONS: dict = None

        def toJSON(self) -> str:
            return json.dumps(asdict(self))

## DB QUERIES
## __________________________________________________________________________________________________

def SQL_BY_ROW(TABLE: str, ID):
    return execute_query(conn.table(TABLE).select('*').like("Id", ID)).data

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

def GET_LOCAL_DB() -> None:
    path_file = "flexical.db"
    if os.path.exists(path_file):
        os.remove(path_file)
    
    ## SQLITE
    conn_sqlite = sqlite3.connect(path_file)
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
        SQL = f"""INSERT INTO MODELS ('Id', 'MODEL', 'MANUFACTURER', 'DEVICE_TYPE', 'DESCRIPTION', 'INFO', 'DB', 'FIRM') VALUES ('{e['Id']}', '{e['MODEL']}', '{e['MANUFACTURER']}', '{e['DEVICE_TYPE']}', '{e['DESCRIPTION']}', '{e['INFO']}', '{e['DB']}', '{e['FIRM']}');"""
        cur_sqlite.execute(SQL)
    conn_sqlite.commit()
    cur_sqlite.close()
    conn_sqlite.close()
    
    ## FIN
    sleep(2)