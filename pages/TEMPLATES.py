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

def TEST_EDITOR(DB: dict) -> None:
    
    col_config = {
        # "✔️": st.column_config.CheckboxColumn(width='small'),
        "TEST": st.column_config.TextColumn(),
        "TEST_INFO": st.column_config.TextColumn(),
        "CONFIG": st.column_config.TextColumn(),
        "PROCEDURE_ID": st.column_config.SelectboxColumn(options=[procedure for procedure in SQL_SELECT_COLUMN("PROCEDURES", "Id")]),
    }

    serie = {
        "TEST": 'st.colu',
        "TEST_INFO": 'st',
        "CONFIG": 'st.co',
        "PROCEDURE_ID": "VDC_METERS"
    }
    l = [serie]

    DF = pd.DataFrame(l, columns=list(col_config.keys()))
    # DF.insert(0, "✔️", False)

    col12, col22 = st.columns([9,1])
    with col12:
        TBL_TEST = st.dataframe(
            data=DF, 
            hide_index=True,
            # num_rows='dynamic',
            column_config=col_config,
            use_container_width=True,
            selection_mode='multi-row',
        )

        people = TBL_TEST.selection
        # filtered_df = DF.iloc[people]
        # st.dataframe(
        #     filtered_df,
        #     column_config=col_config,
        #     use_container_width=True,
        # )
        st.write(TBL_TEST.selection)

        # new_tbl = TBL_TEST[TBL_TEST["✔️"]]
        # new_tbl = new_tbl.reset_index()
        # del new_tbl['index']
        # del new_tbl["✔️"]
        # st.write(new_tbl)

    with col22:
        with st.popover(label=USUAL_ICONS.EXPANDER.value):
            btn_test_add = st.button(label='➕ ADD TEST', use_container_width=True)
            btn_test_del = st.button(label='➖ DEL TEST', use_container_width=True)
    
    if btn_test_add:
        # @st.experimental_dialog(title='✏️ EDITOR', width='large')
        # def FORM():
        #     
        pass
        
    btn_update = st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key='btn_update')


    # print(TBL_TEST)

    # # Filter the dataframe using the temporary column, then drop the column
    # selected_rows = TBL_TEST[TBL_TEST["SELECT"]]
    # # selected_rows = TBL_TEST.drop(".", axis=1)

    # SELECTED: str = None
    # if len(selected_rows) == 1:
    #     SELECTED = selected_rows.iloc[0]

    # return SELECTED


## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

if 'PROCEDURES' not in st.session_state:
    st.session_state.PROCEDURES = 1

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


    ## TEST LIST
    ## __________________________________________________________________________________________________

    st.text("") # SEPARATOR
    # st.markdown(''':blue-background[💊 CMC:]''')
    st.subheader('TEST LIST:', divider='blue')

    if not CURRENT_TEMPLATE["DB"].get("TEST_LIST"):
        CURRENT_TEMPLATE["DB"]["TEST_LIST"] = {}

    selected = TEST_EDITOR(CURRENT_TEMPLATE["DB"])
    st.write(selected)


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




## Dataframe selections / https://docs.streamlit.io/develop/api-reference/data/st.dataframe
## __________________________________________________________________________________________________

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        np.random.randn(12, 5), columns=["a", "b", "c", "d", "e"]
    )

event = st.dataframe(
    st.session_state.df,
    key="data",
    on_select="rerun",
    selection_mode=["multi-row", "multi-column"],
)

event.selection