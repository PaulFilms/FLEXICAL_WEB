'''
FLEXICAL v3 | DATABASE

`SUPABASE INFO:`
    pip install st-supabase-connection
    https://docs.streamlit.io/develop/tutorials/databases/supabase
    https://github.com/SiddhantSadangi/st_supabase_connection

'''

## PYTHON LIBRARIES
import os, json, sqlite3
from datetime import datetime
from dataclasses import dataclass, asdict, fields
from enum import Enum
from typing import TypedDict
from time import sleep

## IMPORTED LIBRARIES
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query



## DB CONNECTION
## __________________________________________________________________________________________________

conn = st.connection("supabase", type=SupabaseConnection, ttl=None)



## DATACLASSES
## __________________________________________________________________________________________________

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



## FUNCTIONS
## __________________________________________________________________________________________________

def GET_FIRM() -> str:
    date_now = datetime.now().strftime("%Y-%m-%d / %H:%M")
    return f"{st.session_state.LOGIN_STATUS} [{date_now}]"



## DB QUERIES
## __________________________________________________________________________________________________

def SQL_BY_ROW(TABLE: str, FIELD: str, VALUE):
    return execute_query(conn.table(TABLE).select('*').eq(FIELD, VALUE)).data

def SQL_ID_COUNT(TABLE: str, ID: str) -> int:
    return execute_query(conn.table(TABLE).select('*', count='exact').like("Id", ID)).count

def SQL_SELECT_COLUMN(TABLE: str, COLUMN: str) -> list:
    SQL = execute_query(conn.table(TABLE).select(COLUMN).order(COLUMN))
    return [data[COLUMN] for data in SQL.data]

def SQL_SELECT_DB(TABLE: str, ID: str):
    SQL = execute_query(conn.table(TABLE).select('DB').eq('Id', ID)).data
    return SQL[0]['DB']

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
def SQL_TEMPLATES_VIEW(COUNT: int) -> list:
    print(f"SQL TEMPLATES_VIEW ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("TEMPLATES_VIEW").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_CUSTOMERS(COUNT: int):
    print(f"SQL CUSTOMERS ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("CUSTOMERS").select('*').order("Id"), ttl="10m")
    return SQL.data

@st.cache_resource
def SQL_COMPANIES(COUNT: int):
    print(f"SQL DEVICES ({COUNT}):", GET_FIRM())
    SQL = execute_query(conn.table("DEVICES").select('*').order("Id"), ttl="10m")
    return SQL.data

def SQL_INSERT(TABLE: str, VALUES: dict) -> None:
    execute_query(conn.table(TABLE).insert([VALUES]), ttl=0)

def SQL_UPDATE_ID(TABLE: str, ID, FIELD: tuple[str, any]):
    execute_query(conn.table(TABLE).update({FIELD[0]: FIELD[1], "FIRM": GET_FIRM()}).eq("Id", ID), ttl=0)
    if TABLE not in st.session_state:
        st.session_state[TABLE] = 1
    st.session_state[TABLE] += 1

def SQL_UPDATE_DB(TABLE: str, ID, DB: dict) -> None:
    execute_query(conn.table(TABLE).update({"DB": json.dumps(DB), "FIRM": GET_FIRM()}).eq("Id", ID), ttl=0)
    if TABLE not in st.session_state:
        st.session_state[TABLE] = 1
    st.session_state[TABLE] += 1

def GET_LOCAL_DB() -> None:
    '''
    INCOMPLETE:

    TASK:

    TBL COMPANIES / CUSTOMERS
    TBL PROCEDURES
    TBL TEMPLATES / VIEW with models datas
    TBL DEVICES VIEW (Only Local Calibrations)
    
    '''
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