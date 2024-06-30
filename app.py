'''
FLEXICAL v3 | MENU

`INFO:`

https://docs.streamlit.io/develop/tutorials/multipage/st.page_link-nav

Info about login
https://github.com/mkhorasani/Streamlit-Authenticator
pip install streamlit-authenticator

'''

## PYTHON LIBRARIES
import os, json
from io import StringIO
from typing import Union, Tuple
from dataclasses import dataclass
from enum import Enum, auto

## IMPORTED LIBRARIES
import pandas as pd
import numpy as np

## STREAMLIT
import streamlit as st
# st.set_page_config(
#     page_title="FLEXICAL DEVELOPER",
#     page_icon=":guardsman:",
#     layout="wide", # "centered",
#     initial_sidebar_state= "auto" # "collapsed"
# )

## INTERNAL
from db import SQL_UPDATE_ID, SQL_UPDATE_DB



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
    PRINT = "🖨️"

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


## FUNCTIONS
## __________________________________________________________________________________________________


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
        st.sidebar.page_link(r"pages/HOME.py", label="🏠 HOME") #, icon="🏠")
        # if st.session_state.page != "DATABASE":
            # if st.sidebar.button(label="📦 DB ITEMS", use_container_width=True):
                # st.switch_page(r"pages/DATABASE.py")
        st.sidebar.page_link(r"pages/DATABASE.py", label="DB ITEMS", icon="📦")

        ## EDITOR PAGES
        st.sidebar.text("")
        with st.sidebar.expander("__✏️ EDITORS__", expanded=True):
            st.text("")
            st.page_link(r"pages/PROCEDURES.py", label="PROCEDURES", use_container_width=True)
            st.page_link(r"pages/MODELS.py", label="MODELS") # , icon="🚗"
            st.page_link(r"pages/TEMPLATES.py", label="TEMPLATES", use_container_width=True)
            st.page_link(r"pages/CALIBRATIONS.py", label="CALIBRATIONS", use_container_width=True)

    else: 
        # if st.sidebar.button("🪪 LOGIN", use_container_width=True):
        st.switch_page(r"pages/LOGIN.py")

def INFO_EDITOR(TABLE: str, ID: str, INFO: str) -> None:
    col12, col22 = st.columns([9,1])
    with col12:
        with st.container(border=True):
            st.markdown(body=INFO)
    with col22:
        with st.popover(label=USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button(label='✏️ EDITOR', use_container_width=True, key='INFO_EDITOR')
    
    @st.experimental_dialog(title='✏️ EDITOR', width='large')
    def EDITOR():
        NEW_INFO = st.text_area(label="tx_markdown_raw", value=INFO, height=400, label_visibility='collapsed')
        if st.button(label="🔄 UPDATE"):
            try:
                SQL_UPDATE_ID(TABLE, ID, ("INFO", NEW_INFO))
                st.session_state[TABLE] += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)
    
    if btn_editor: EDITOR()

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

def TBL_EDITOR(DATAFRAME: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
    '''
    Render a st.data_editor with the basics fields to use for calculation
    RANGE1, RANGE2, EVALUATION, C1, C2, C3 ...
    '''
    with st.popover(USUAL_ICONS.EXPANDER.value):
        tg_format = st.toggle('FORMAT DECIMAL', value=False)
        tg_checker = st.toggle('CHECKER', value=False)

    if "tbl_float_format" not in st.session_state:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format="%.2e")
    
    if tg_format:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format=None)
    else:
        st.session_state.tbl_float_format = st.column_config.NumberColumn(format="%.2e")

    DATAFRAME['RANGE1_MIN'] = DATAFRAME['RANGE1_MIN'].astype(float)
    DATAFRAME['RANGE1_MAX'] = DATAFRAME['RANGE1_MAX'].astype(float)
    DATAFRAME['RANGE2_MIN'] = DATAFRAME['RANGE2_MIN'].astype(float)
    DATAFRAME['RANGE2_MAX'] = DATAFRAME['RANGE2_MAX'].astype(float)
    DATAFRAME['C1'] = DATAFRAME['C1'].astype(float)
    DATAFRAME['C2'] = DATAFRAME['C2'].astype(float)
    DATAFRAME['C3'] = DATAFRAME['C3'].astype(float)
    DATAFRAME['EVALUATION'] = DATAFRAME['EVALUATION'].astype(str)
    DATAFRAME.insert(len(DATAFRAME.columns)-1, 'EVALUATION', DATAFRAME.pop('EVALUATION'))
    DATAFRAME = DATAFRAME.reset_index()
    del DATAFRAME['index']

    column_config = dict()
    for column in list(DATAFRAME.columns):
        if DATAFRAME[column].dtype == np.float64:
            # print("FLOAT")
            column_config[column] = st.session_state.tbl_float_format
    column_config['EVALUATION'] = st.column_config.TextColumn(default="(VALUE1*C1*1e1) + (C2*1e1) # VALUE1(<unit>), VALUE2(null)")

    TABLE_EDITOR = st.data_editor(
        DATAFRAME,
        hide_index=True,
        num_rows='dynamic',
        # column_config={
        #     'RANGE1_MIN': st.session_state.tbl_float_format,
        #     'RANGE1_MAX': st.session_state.tbl_float_format,
        #     'RANGE2_MIN': st.session_state.tbl_float_format,
        #     'RANGE2_MAX': st.session_state.tbl_float_format,
        #     'C1': st.session_state.tbl_float_format,
        #     'C2': st.session_state.tbl_float_format,
        #     'C3': st.session_state.tbl_float_format,
        #     'EVALUATION': st.column_config.TextColumn(default="(VALUE1*C1*1e1) + (C2*1e1) # VALUE2"),
        # },
        column_config=column_config,
        use_container_width=True
    )

    if tg_checker:
        with st.container(border=False):
            col13, col23, col33 = st.columns([1,1,2])
            with col13:
                VALUE1 = st.number_input("VALUE1", label_visibility='collapsed', min_value=TABLE_EDITOR['RANGE1_MIN'].min(), max_value=TABLE_EDITOR['RANGE1_MAX'].max())
            with col23:
                VALUE2 = st.number_input("VALUE2", label_visibility='collapsed', min_value=TABLE_EDITOR['RANGE2_MIN'].min(), max_value=TABLE_EDITOR['RANGE2_MAX'].max())
            with col33:
                result = str()
                if VALUE1: result += f'VALUE1: {VALUE1} | '
                if VALUE2 and not pd.isnull(VALUE2): result += f'VALUE2: {VALUE2} | '
                RESULT = TABLE_DATA.GET_VALUE(TABLE_EDITOR, VALUE1, VALUE2)
                if RESULT:  result += f'RESULT: {RESULT:.2E}'
                else: result += f'RESULT: --'
                st.text(result)
    
    btn_update = st.button(USUAL_ICONS.UPDATE.value + " UPDATE", key="TBL_EDITOR")
    
    return TABLE_EDITOR, btn_update

class RESULTS:
    '''
    Set of Functions and Classes to Get and Define a Result of a Calibration
    
    `Info:`
        - BUG: No trabajar con pandas
    '''
    class TYPES(Enum):
        CHECK = 0
        MEASURE = auto()
        DEVIATION = auto()
        MAXIMUN = auto()
        MINIMUN = auto()
        REFERENCE = auto()

def DB_EDITOR(TABLE: str, ID: str, DB: dict):
    col12, col22 = st.columns([9,1])
    with col12:
        with st.container(border=True):
            st.json(DB, expanded=False)
    with col22:
        with st.popover(USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button('✏️ EDITOR', use_container_width=True, key='DB_EDITOR')

    @st.experimental_dialog('✏️ EDITOR', width='large')
    def EDITOR():
        col12, col22 = st.columns(2)
        with col12:
            NEW_ITEM = st.text_input("NEW ITEM", label_visibility='collapsed')
        with col22:
            btn_newitem = st.button("INSERT NEW ITEM")
        if btn_newitem:
            if NEW_ITEM in DB:
                INFOBOX("THIS ITEM IS ALREADY IN THE DB")
            else:
                DB[NEW_ITEM] = None
        
        st.divider()
        st.text("SELECT ITEM")
        col12, col22 = st.columns(2)
        with col12:
            ITEM = st.selectbox("EDIT ITEM", options=list(DB.keys()), label_visibility='collapsed')
        with col22:
            btn_deleteitem = st.button("DELETE ITEM")
        if ITEM and btn_deleteitem:
            del DB[ITEM]
            SQL_UPDATE_DB(TABLE, ID, DB)
            st.rerun()
        if ITEM:
            TEXT = st.text_area("CONTENT", DB[ITEM])
            VALUE = None
            col12, col22 = st.columns(2)
            with col12:
                VALIDATION = st.selectbox("VALIDATION", options=["BOOL", "TEXT", "NUMBER", "JSON"], label_visibility='collapsed')
            with col22:
                btn_validate = st.button("VALIDATE")
            holder_update = st.empty()

            def VALIDATE():
                try:
                    match VALIDATION:
                        case "BOOL": VALUE = bool(TEXT)
                        case "TEXT": VALUE = str(TEXT)
                        case "NUMBER": VALUE = float(TEXT)
                        case "JSON": 
                            VALUE = TEXT.replace(chr(39), chr(34))
                            VALUE = VALUE.replace("None", "null")
                            VALUE = VALUE.replace("nan", "null")
                            VALUE = dict(json.loads(VALUE))
                            # VALUE = json.dumps(VALUE)
                    st.success(VALUE)
                    holder_update.button("UPDATE")
                except Exception as e:
                    INFOBOX(e)
                    VALUE = None
                return VALUE

            if btn_validate:
                VALIDATE()

            # btn_update = st.button("🔄 UPDATE")
            # if btn_update:
            #     NEW_VALUE = VALIDATE()
            #     print("UPDATE", NEW_VALUE)
            #     st.rerun()

            # if btn_update:
            #     DB[ITEM] = VALUE
            #     print("UPDATE", DB)
            #     SQL_UPDATE_DB(TABLE, ID, DB)
            #     st.rerun()
            if holder_update:
                print("UPDATE")
                st.rerun()

    
    if btn_editor: EDITOR()

def PYDATA_EDITOR(TABLE: str, ID: str, PYDATA: str):
    col12, col22 = st.columns([9,1])
    with col12:
        st.code(PYDATA, language='python')
    with col22:
        with st.popover(USUAL_ICONS.EXPANDER.value):
            btn_editor = st.button('✏️ EDITOR', use_container_width=True, key='PYDATA_EDITOR_EDITOR')
            st.download_button(
                    label=USUAL_ICONS.SAVE.value + " EXPORT .py",
                    data=PYDATA,
                    file_name=f"{ID}.py",
                    mime="application/python",
                    use_container_width=True
                )

    @st.experimental_dialog('✏️ EDITOR', width='large')
    def EDITOR():
        new_data = PYDATA
        ## FROM .PY
        uploaded_file = st.file_uploader("CHOOSE A PYTHON FILE:", accept_multiple_files=False, type='py', key="file_uploader")
        if uploaded_file is not None:
            ## To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            new_data = string_data
        NEW_INFO = st.text_area("TEXT EDITOR:", new_data, height=400)
        if st.button("🔄 UPDATE", key="PYDATA_EDITOR_UPDATE"):
            print("UPDATE PYDATA")
            try:
                SQL_UPDATE_ID(TABLE, ID, ("PYDATA", NEW_INFO))
                st.session_state[TABLE] += 1
                st.rerun()
            except Exception as e:
                INFOBOX(e)

    if btn_editor: EDITOR()

## TEMP
## __________________________________________________________________________________________________

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
    def GET_VALUE(DATAFRAME: pd.DataFrame, VALUE1: Union[int, float], VALUE2: Union[int, float] = None, ABS: bool = True) -> float:
        '''
        Returns a calculated value from the selected DataFrame

        `Args:`
            - DATAFRAME: pd.DataFrame
            - VALUE1: Union[int, float]
            - VALUE2: Union[int, float]
            - **ABS: bool = True (Default)
        '''
        ## ABS VALUES
        if ABS:
            VALUE1 = abs(VALUE1)
            if VALUE2:
                VALUE2 = abs(VALUE2)
        
        ## CHECK DATA FRAME
        if not all(field.name in DATAFRAME.columns for field in TABLE_DATA.FIELDS):
            # print("TBL_CALC: Necessary fields not available")
            return None
        
        ## RANGE 1
        if VALUE1 == None or pd.isnull(VALUE1):
            return None
        if VALUE1 == DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name].min():
            DF_FILTER: pd.DataFrame = DATAFRAME[DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name] == VALUE1]
        else:
            cond1 = (VALUE1 > DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name])
            cond2 = (VALUE1 <= DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MAX.name])
            DF_FILTER: pd.DataFrame = DATAFRAME[cond1 & cond2]
        if len(DF_FILTER) == 0:
            return None

        ## RANGE 2
        check1: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MIN.name].min())
        check2: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MAX.name].max())
        if check1 == False or check2 == False:
            if VALUE2 == None or pd.isnull(VALUE2):
                return None
            if VALUE2 == DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name].min():
                DF_FILTER = DF_FILTER[DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name] == VALUE2]
            else:
                cond1 = (VALUE2 > DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name])
                cond2 = (VALUE2 <= DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MAX.name])
                DF_FILTER = DF_FILTER[cond1 & cond2]
            if len(DF_FILTER) != 1:
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
    
    def FILTER_VALUE(DATAFRAME: pd.DataFrame, COLUMN: str, VALUE1: Union[int, float], VALUE2: Union[int, float] = None, ABS: bool = True) -> float:
        '''
        '''
        ## ABS VALUES
        if ABS:
            VALUE1 = abs(VALUE1)
            if VALUE2:
                VALUE2 = abs(VALUE2)

        ## CHECK DATA FRAME
        if not all(field.name in DATAFRAME.columns for field in TABLE_DATA.FIELDS):
            # print("TBL_CALC: Necessary fields not available")
            return None
        
        ## RANGE 1
        if VALUE1 == None or pd.isnull(VALUE1):
            return None
        if VALUE1 == DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name].min():
            DF_FILTER: pd.DataFrame = DATAFRAME[DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name] == VALUE1]
        else:
            cond1 = (VALUE1 > DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MIN.name])
            cond2 = (VALUE1 <= DATAFRAME[TABLE_DATA.FIELDS.RANGE1_MAX.name])
            DF_FILTER: pd.DataFrame = DATAFRAME[cond1 & cond2]
        if len(DF_FILTER) == 0:
            return None

        ## RANGE 2
        check1: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MIN.name].min())
        check2: bool = pd.isnull(DATAFRAME[TABLE_DATA.FIELDS.RANGE2_MAX.name].max())
        if check1 == False or check2 == False:
            if VALUE2 == None or pd.isnull(VALUE2):
                return None
            if VALUE2 == DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name].min():
                DF_FILTER = DF_FILTER[DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name] == VALUE2]
            else:
                cond1 = (VALUE2 > DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MIN.name])
                cond2 = (VALUE2 <= DF_FILTER[TABLE_DATA.FIELDS.RANGE2_MAX.name])
                DF_FILTER = DF_FILTER[cond1 & cond2]
            if len(DF_FILTER) != 1:
                return None

        return DF_FILTER.iloc[0][COLUMN]

@dataclass
class UNIT:
    '''
    Internal class to define the equivalent value of a unit with its base unit and its multiplication factor
    '''
    unit: str
    factor: int

class UNITS(Enum):
    '''
    Enumeration class with some units in text format with their equivalent in base unit
    
    `Examples:`
    - V = UNIT("V", 1)
    - kV = UNIT("V", 1e3)
    '''
    ## VOLTS
    nV = UNIT("V", 1e-9)
    𝝻V = UNIT("V", 1e-6)
    uV = UNIT("V", 1e-6)
    mV = UNIT("V", 1e-3)
    V = UNIT("V", 1)
    kV = UNIT("V", 1e3)
    MV = UNIT("V", 1e6)
    GV = UNIT("V", 1e9)
    ## AMPS
    nA = UNIT("A", 1e-9)
    𝝻A = UNIT("A", 1e-6)
    uA = UNIT("A", 1e-6)
    mA = UNIT("A", 1e-3)
    A = UNIT("A", 1)
    kA = UNIT("A", 1e3)
    MA = UNIT("A", 1e6)
    ## OHMS
    nOhm = UNIT("Ω", 1e-9)
    𝝻Ohm = UNIT("Ω", 1e-6)
    uOhm = UNIT("Ω", 1e-6)
    mOhm = UNIT("Ω", 1e-3)
    Ohm = UNIT("Ω", 1)
    kOhm = UNIT("Ω", 1e3)
    MOhm = UNIT("Ω", 1e6)
    GOhm = UNIT("Ω", 1e9)
    nΩ = UNIT("Ω", 1e-9)
    𝝻Ω = UNIT("Ω", 1e-6)
    uΩ = UNIT("Ω", 1e-6)
    mΩ = UNIT("Ω", 1e-3)
    Ω = UNIT("Ω", 1)
    kΩ = UNIT("Ω", 1e3)
    MΩ = UNIT("Ω", 1e6)
    GΩ = UNIT("Ω", 1e9)
    ## WATTS
    𝝻W = UNIT("W", 1e-6)
    uW = UNIT("W", 1e-6)
    mW = UNIT("W", 1e-3)
    W = UNIT("W", 1)
    kW = UNIT("W", 1e3)
    MW = UNIT("W", 1e6)
    ## HERTZ
    nHz = UNIT("Hz", 1e-9)
    𝝻Hz = UNIT("Hz", 1e-6)
    uHz = UNIT("Hz", 1e-6)
    mHz = UNIT("Hz", 1e-3)
    Hz = UNIT("Hz", 1)
    kHz = UNIT("Hz", 1e3)
    MHz = UNIT("Hz", 1e6)
    GHz = UNIT("Hz", 1e9)
    ## SECONDS
    ns = UNIT("s", 1e-9)
    𝝻s = UNIT("s", 1e-6)
    us = UNIT("s", 1e-6)
    ms = UNIT("s", 1e-3)
    s = UNIT("s", 1)
    ## dB
    dB = UNIT("dB", 1)
    dBm = UNIT("dBm", 1)
    dBc = UNIT("dBc", 1)
    
    @classmethod
    def to_base(cls, value: float, unit: Union['UNITS', str]) -> float:
        '''
        Specific Function to convert a value to base unit

        `Args:`
            value <float>: Selected value
            unit <str> | <UNITS>: Unit of selected value
        
        `Retrurns:`
            <float> Converted value in base unit
        
        `Examples: `
            - value=123.456, unit="mW" = 0.123456 (W)
            - value=123.456, unit=UNITS.mW = 0.123456 (W)
        '''
        unit_type = type(unit)
        if unit_type == str:
            return value * cls[unit].value.factor
        elif unit_type == UNITS:
            return value * unit.value.factor
    
    @classmethod
    def from_base(cls, base_value: Union[int, float], unit: Union['UNITS', str]) -> float:
        '''
        Specific Function to convert a value from base unit

        `Args:`
            value <float>: Selected value
            unit <str> | <UNITS>: Unit of selected value
        
        `Retrurns:`
            <float> Converted value in selected unit
        
        `Examples: `
            - value=123.456, unit="mW" = 123456.0 (mW)
            - value=123.456, unit=UNITS.mW = 123456.0 (mW)
        '''
        if isinstance(base_value, str):
            return 0.0
        if isinstance(unit, type(None)):
            return 0.0
        if isinstance(unit, str):
            return base_value / cls[unit].value.factor
        if isinstance(unit, UNITS):
            return base_value / unit.value.factor



## APP
## __________________________________________________________________________________________________

if __name__ == "__main__":
    st.switch_page(r"pages/LOGIN.py")
