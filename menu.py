'''
FLEXICAL v3 | MENU

`INFO:`

https://docs.streamlit.io/develop/tutorials/multipage/st.page_link-nav

Info about login
https://github.com/mkhorasani/Streamlit-Authenticator
pip install streamlit-authenticator

'''

## PYTHON LIBRARIES
import os
from typing import Union
from datetime import datetime
from enum import Enum, auto

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd



## COMPONENTS
## __________________________________________________________________________________________________

path_resources = r"resources"

class USUAL_ICONS(Enum): # 🪪🧮
    HOME = "🏠"
    EXIT = "⛔"
    SAVE = "💾"
    DELETE = "🗑️"
    INSERT = "➕"
    UPDATE = "🔄"
    CHECK = "✅" # ✔️ ✅
    WARNINNG = "🚨" # 🚨 🚩 ⚠️
    UP = "🔼"
    DOWN = "🔽"
    QUESTION = "❓"
    EXPANDER = chr(8801)
    LOCK = "🔒"
    LOGIN = "🪪"

def FOOTER(TEXT: str):
    footer = """<style>.footer {position: fixed;left: 330;bottom: 0;width: 100%;background-color: #000;color: white;text-align: left;}</style><div class='footer'><p>"""
    footer += TEXT
    footer += """</p></div>"""
    return st.markdown(footer, unsafe_allow_html=True)

def INFOBOX(info: str):
    return st.warning(info, icon="🚨")

@st.experimental_dialog(title="❓")
def YESNOBOX(info: str, FUNCTION):
    st.text(info)
    col12, col22 = st.columns(2)
    with col12:
        if st.button("YES", use_container_width=True):
            FUNCTION()
            st.rerun()
    with col22:
        if st.button("NO", use_container_width=True):
            st.rerun()

def COL_SCI(label: str):
    return st.column_config.NumberColumn(label=label, format="%.2e")

def DATAFRAME_LIST(DATAFRAME: pd.DataFrame, COLUMN: str) -> tuple[pd.DataFrame, str]:
    '''
    Obtiene desde una columna de un data frame, otro dataframe con una columna seleccionable y el item seleccionado
    '''
    df_with_selections = DATAFRAME.copy()
    df_with_selections.insert(0, "✔️", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            "✔️": st.column_config.CheckboxColumn(required=True, width='small'),
            COLUMN: st.column_config.TextColumn(required=True, width='large'),
        },
        disabled=DATAFRAME.columns,
        use_container_width=True
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df["✔️"]]
    selected_rows.drop("✔️", axis=1)

    SELECTED: str = None
    if len(selected_rows) == 1:
        SELECTED = selected_rows[COLUMN].iloc[0]

    return edited_df, SELECTED



## FUNCTIONS
## __________________________________________________________________________________________________

def GET_FIRM() -> str:
    date_now = datetime.now().strftime("%Y-%m-%d / %H:%M")
    return f"{st.session_state.LOGIN_STATUS} [{date_now}]"



## MENUS
## __________________________________________________________________________________________________

# st.sidebar.page_link("app.py", label="HOME", icon="🏠")
# st.sidebar.page_link(r"pages/PROFILE.py", label=":blue-background[PROFILE]", icon="🧬", use_container_width=True)
# st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
# st.sidebar.page_link(r"pages/MANUFACTURERS.py", label="MANUFACTURERS", icon="🚗")
# st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")
# st.sidebar.page_link(r"pages/PROCEDURES.py", label=":blue-background[PROCEDURES]", icon="🧬", use_container_width=True)
# st.sidebar.page_link(r"pages/TEMPLATES.py", label=":blue-background[TEMPLATES]", icon="🧬", use_container_width=True)


def SIDEBAR():
    st.logo(os.path.join(path_resources, r"LOGO2.svg"))
    if 'LOGIN_STATUS' not in st.session_state:
        st.session_state.LOGIN_STATUS = None
    if st.session_state.LOGIN_STATUS:
        with st.sidebar.expander(f"🌐 {st.session_state.LOGIN_STATUS}", expanded=False): # use_container_width=True
            if st.button(f"{USUAL_ICONS.EXIT.value} [LOG OUT]", use_container_width=True, help="Logout"):
                st.session_state.LOGIN_STATUS = None
                st.switch_page(r"app.py")
            # if st.button("⚙️ PROFILE", use_container_width=True):
            #     st.switch_page(r"pages/PROFILE.py")
            st.page_link(r"pages/PROFILE.py", label="PROFILE", icon="⚙️")
        st.sidebar.text("")
        # if st.session_state.page != "HOME":
        st.sidebar.page_link("app.py", label="🏠 HOME") #, icon="🏠")
        # if st.session_state.page != "DATABASE":
            # if st.sidebar.button(label="📦 DB ITEMS", use_container_width=True):
                # st.switch_page(r"pages/DATABASE.py")
        st.sidebar.page_link(r"pages/DATABASE.py", label="DB ITEMS", icon="📦")
        # SB_EDITORS()
        st.sidebar.text("")
        with st.sidebar.expander("__✏️ EDITORS__", expanded=True):
            st.text("")
            st.page_link(r"pages/MODELS.py", label="MODELS") # , icon="🚗"
            st.page_link(r"pages/PROCEDURES.py", label="PROCEDURES", use_container_width=True)
            st.page_link(r"pages/TEMPLATES.py", label="TEMPLATES", use_container_width=True)
            st.page_link(r"pages/CALIBRATIONS.py", label="CALIBRATIONS", use_container_width=True)

    else: 
        # if st.sidebar.button("🪪 LOGIN", use_container_width=True):
        st.switch_page(r"pages/LOGIN.py")

# def SB_EDITORS():
#     st.sidebar.text("")
#     with st.sidebar.expander("__✏️ EDITORS__", expanded=True):
#         st.text("")
#         st.page_link(r"pages/MODELS.py", label="MODELS") # , icon="🚗"
#         st.page_link(r"pages/PROCEDURES.py", label="PROCEDURES", use_container_width=True)
#         st.page_link(r"pages/TEMPLATES.py", label="TEMPLATES", use_container_width=True)
#         st.page_link(r"pages/CALIBRATIONS.py", label="CALIBRATIONS", use_container_width=True)



## TEMP
## __________________________________________________________________________________________________


# from streamlit import runtime
# from streamlit.runtime.scriptrunner import get_script_run_ctx

# def get_remote_ip() -> str:
#     """Get remote ip."""

#     try:
#         ctx = get_script_run_ctx()
#         if ctx is None:
#             return None

#         session_info = runtime.get_instance().get_client(ctx.session_id)
#         if session_info is None:
#             return None
#     except Exception as e:
#         return None

#     return session_info.request.remote_ip

# from streamlit.web.server.websocket_headers import _get_websocket_headers

class TABLE_DATA:
    '''
    Class to get value of a DataFrame based on two Ranges

    `Fields:`
        - RANGE1_MIN
        - RANGE1_MAX
        - RANGE2_MIN
        - RANGE2_MAX
        - EVALUATION
        - [CONTRIBUTIONS]
    
    `Functions:`
        - GET_VALUE
    '''
    class FIELDS(Enum):
        '''
        Fixed fields into a data table
        '''
        RANGE1_MIN = 0
        RANGE1_MAX = auto()
        RANGE2_MIN = auto()
        RANGE2_MAX = auto()
        EVALUATION = auto()
    
    @staticmethod
    def GET_VALUE(DATAFRAME: pd.DataFrame, VALUE1: Union[int, float], VALUE2: Union[int, float] = None) -> float:
        '''
        Returns a calculated value from the selected DataFrame

        `Args:`
            - DATAFRAME: pd.DataFrame
            - VALUE1: Union[int, float]
            - VALUE2: Union[int, float]
        '''
        ## CHECK DATA FRAME
        if not all(field.name in DATAFRAME.columns for field in TABLE_DATA.FIELDS):
            # print("TBL_CALC: Necessary fields not available")
            return None
        
        ## RANGE 1
        if VALUE1 == None or VALUE1 == 0 or pd.isnull(VALUE1):
            return None
        if DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name].min() == VALUE1:
            DF_FILTER: pd.DataFrame = DATAFRAME[DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name] == VALUE1]
        else:
            cond1 = (VALUE1 > DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name])
            cond2 = (VALUE1 <= DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MAX.name])
            DF_FILTER: pd.DataFrame = DATAFRAME[cond1 & cond2]
        if len(DF_FILTER) == 0:
            # print("TBL_CALC: Length Filter from VALUE1 = 0")
            return None

        ## RANGE 2
        check1: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MIN.name].min())
        check2: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MAX.name].max())
        if check1 == False or check2 == False:
            if VALUE2 == None or VALUE2 == 0 or pd.isnull(VALUE2):
                return None
            if DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name].min() == VALUE2:
                DF_FILTER = DF_FILTER[DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name] == VALUE2]
            else:
                cond1 = (VALUE2 > DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name])
                cond2 = (VALUE2 <= DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MAX.name])
                DF_FILTER = DF_FILTER[cond1 & cond2]
            if len(DF_FILTER) != 1:
                # print("TBL_CALC ERROR: Length Filter from VALUE2 != 1")
                return None

        ## EVAL
        EVALUATION: str = DF_FILTER.iloc[0][TABLE_DATA.FIELDS.EVALUATION.name]
        if pd.isnull(EVALUATION):
            print("TBL_CALC ERROR: EVALUATION IS NULL")
            return None
        try:
            for key, value in DF_FILTER.iloc[0].to_dict().items():
                if pd.isnull(value):
                    globals()[key] = 0
                else: 
                    globals()[key] = value
            return eval(EVALUATION)
        except Exception as e:
            print("TBL_CALC ERROR:")
            print(e)
            return None