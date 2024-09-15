from enum import Enum
from datetime import datetime
import streamlit as st

# from st_supabase_connection import SupabaseConnection, execute_query
# conn = st.connection("supabase", type=SupabaseConnection, ttl=None)

# from st_supabase_connection import SupabaseConnection
# conn = st.connection("supabase",type=SupabaseConnection, ttl='10m')

from supabase import create_client, Client

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data() # ttl=600
# def run_query():
#     return supabase.table("TEMPLATES").select("Id").execute()

class TABLES(Enum):
    COMPANIES = "COMPANIES"
    DEVICE_TYPES = "DEVICE_TYPES"
    MANUFACTURERS = "MANUFACTURERS"
    MODELS = "MODELS"
    DEVICES = "DEVICES"
    PROCEDURES = "PROCEDURES"
    TEMPLATES = "TEMPLATES"

def get_firm() -> str:
    date_now = datetime.now().strftime("%Y-%m-%d / %H:%M")
    return f"{st.session_state.role.name} [{date_now}]"

@st.cache_resource
def sql_table(table: str, count: int):
    print(f"SQL {table} ({count}):", get_firm())
    return supabase.table(table).select('*').order("Id").execute().data