'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from dataclasses import asdict
from enum import Enum

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import *
from db import *


## MENU
## __________________________________________________________________________________________________


## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None


class TEMPLATE:

    class TypeDict(TypedDict):
        Id: str
        MODEL_ID: str
        VARSION: str
        INFO: str
        DB: dict
        PYDATA: str

    @dataclass
    class DB:
        TEST_LIST: dict = None

        def toJSON(self) -> str:
            return json.dumps(asdict(self))


## PAGE
## __________________________________________________________________________________________________

# if not st.session_state.LOGIN_STATUS:
#     st.switch_page(r"pages/LOGIN.py")

## SIDEBAR & BASIC COMPONENTS
# st.logo(os.path.join(path_resources, r"LOGO2.svg"))
SIDEBAR()

st.text('TEMPLATE Id')

col12, col22 = st.columns(2)

with col12:
    TEMPLATE_ID = st.selectbox("TEMPLATE Id", options=SQL_SELECT_COLUMN("TEMPLATES", "Id"), index=None, label_visibility='collapsed')

with col22:
    with st.popover(USUAL_ICONS.EXPANDER.value):
        FLTR_DEVICE = st.selectbox("DEVICE TYPE", options=SQL_SELECT_COLUMN("DEVICE_TYPES", "Id"), index=None)
        FLTR_MANUFACTURER = st.selectbox("MANUFACTURER", options=SQL_SELECT_COLUMN("MANUFACTURERS", "Id"), index=None)
        FLTR_MODEL = st.selectbox("MODEL", options=SQL_SELECT_COLUMN("MODELS", "Id"), index=None)


# FOOTER("FLEXICAL | TEMPLATES EDITOR")

if TEMPLATE_ID:
    SQL = SQL_BY_ROW("TEMPLATES", "Id", TEMPLATE_ID)
    # st.json(SQL)
    CURRENT_TEMPLATE = TEMPLATE.TypeDict(**SQL[0])

    if not CURRENT_TEMPLATE["DB"]:
        CURRENT_TEMPLATE["DB"] = asdict(TEMPLATE.DB(TEST_LIST={}))

    ## INFO
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('INFO:', divider='blue')

    INFO_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["INFO"])


    ## TEST
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('TEST:', divider='blue')

    if 'PROCEDURES' not in st.session_state:
        st.session_state.PROCEDURES = 1

    col_config = {
        # ".": st.column_config.CheckboxColumn(),
        "TEST": st.column_config.TextColumn(),
        "TEST_INFO": st.column_config.TextColumn(),
        "CONFIG": st.column_config.TextColumn(),
        "PROCEDURE_ID": st.column_config.SelectboxColumn(options=[procedure for procedure in SQL_SELECT_COLUMN("PROCEDURES", "Id")]),
    }

    DF = pd.DataFrame(columns=list(col_config.keys()))
    TBL_TEST = st.data_editor(
        data=DF, 
        # hide_index=True,
        num_rows='dynamic',
        column_config=col_config,
        use_container_width=True
    )

    # df = pd.DataFrame(
    #     [
    #     {"command": "st.selectbox", "rating": 4, "is_widget": True},
    #     {"command": "st.balloons", "rating": 5, "is_widget": False},
    #     {"command": "st.time_input", "rating": 3, "is_widget": True},
    # ]
    # )
    # edited_df = st.data_editor(df)

    # favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


    ## PYDATA
    ## __________________________________________________________________________________________________

    st.text("")
    st.text("")
    st.subheader('PYDATA:', divider='blue')

    # st.sidebar.markdown("""
    # [➡️ PYDATA](#pydata)
    # """, unsafe_allow_html=True)

    # st.write(CURRENT_TEMPLATE["PYDATA"])
    if not CURRENT_TEMPLATE["PYDATA"]:
        CURRENT_TEMPLATE["PYDATA"] = str()
    
    PYDATA_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["PYDATA"])


    ## DB DATA JSON
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 DB DATA:]''')
    st.subheader('JSON DB DATA:', divider='blue')
    
    DB_EDITOR("TEMPLATES", TEMPLATE_ID, CURRENT_TEMPLATE["DB"])