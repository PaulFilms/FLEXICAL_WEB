'''
FLEXICAL v3 | ...

'''

## PYTHON LIBRARIES
import os
from time import sleep
from typing import TypedDict

## IMPORTED LIBRARIES
import streamlit as st
import pandas as pd

## INTERNAL
from menu import *
from db import *



## SESSION STATES
## __________________________________________________________________________________________________

if 'LOGIN_STATUS' not in st.session_state:
    st.session_state.LOGIN_STATUS = None

if 'PROCEDURES' not in st.session_state:
    st.session_state.PROCEDURES = 1

if 'DB_DATA' not in st.session_state:
    st.session_state.DB_DATA = None


## MENU
## __________________________________________________________________________________________________

class PROCEDURE:
    '''class'''

    class TypeDict(TypedDict):
        Id: str
        TITLE: str
        INFO: str
        DB: dict
        PYDATA: str
        FIRM: str

def get_selected(DATAFRAME: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    df_with_selections = DATAFRAME.copy()
    df_with_selections.insert(0, "✔️", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            "✔️": st.column_config.CheckboxColumn(required=True, width='small'),
            'DEVICE TYPE': st.column_config.TextColumn(required=True, width='large'),
        },
        disabled=DATAFRAME.columns,
        use_container_width=True
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df["✔️"]]
    selected_rows.drop("✔️", axis=1)

    STANDARD: str = None
    if len(selected_rows) == 1:
        STANDARD = selected_rows['DEVICE TYPE'].iloc[0]

    return edited_df, STANDARD


## PAGE
## __________________________________________________________________________________________________

if not st.session_state.LOGIN_STATUS:
    st.switch_page("app.py")

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
# st.image(os.path.join(path_resources, r"procedures.svg"), use_column_width=False)
# st.divider()

SIDEBAR()

st.text("PROCEDURE Id")
col12, col22 = st.columns(2)

with col12:
    # print(SQL_PROCEDURES(1))
    PROCEDURE_ID = st.selectbox("🎛️ PROCEDURE Id", options=[procedure['Id'] for procedure in SQL_PROCEDURES(st.session_state.PROCEDURES)], index=None, label_visibility='collapsed')

if PROCEDURE_ID:
    SQL = SQL_BY_ROW('PROCEDURES', PROCEDURE_ID)

    with col22:
        if st.button("📄 SHOW DOCUMENT", use_container_width=True):
            @st.experimental_dialog("📄 DOCUMENT", width='large')
            def DOCUMENT():
                MD = r'''
                ## PROCEDURE Id
                ---

                Information about procedure


                :blue-background[STANDARDS USED:]
                - Standard 1
                - Standard n

                
                :blue-background[UNCERTAINTY:]

                $$
                u = \sqrt{a^2 + b^2 + c^2}
                $$

                
                :blue-background[CMC:]

                | Column 1      | Column 2      |
                | ------------- | ------------- |
                | Cell 1, Row 1 | Cell 2, Row 1 |
                | Cell 1, Row 2 | Cell 1, Row 2 |

                
                -
                '''
                st.button("PRINT DOCUMENT")
                with st.container(border=True): # height=300, 
                    st.markdown(MD, unsafe_allow_html=True)
            DOCUMENT()

    if len(SQL) != 1:
        st.session_state.DB_DATA = None
        st.warning(f"< {PROCEDURE_ID} > don't exits", icon="⚠️")

    else:
        CURRENT_PROCEDURE = PROCEDURE.TypeDict(**SQL[0])
        CURRENT_DB = CURRENT_PROCEDURE["DB"]
        st.write(CURRENT_PROCEDURE)

        ## DB DATA
        if isinstance(CURRENT_DB, str):
            try:
                st.session_state.DB_DATA = json.loads(CURRENT_DB)
            except:
                st.session_state.DB_DATA = dict()
        elif isinstance(CURRENT_DB, dict):
            st.session_state.DB_DATA = CURRENT_DB
        else:
            st.session_state.DB_DATA = dict()

        ## DATA
        st.text("")
        st.text("")
        st.subheader('DATA:', divider='blue')

        tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE["TITLE"])
        tx_info = st.text_area(label='INFO', value=CURRENT_PROCEDURE["INFO"])


        ## REPORT FORMATS
        st.text("")
        st.text("")
        st.subheader('REPORT FORMATS:', divider='blue')

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 REPORT FORMATS:]''')

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 STANDARDS:]''')

        if not st.session_state.DB_DATA.get('STANDARDS'):
            st.session_state.DB_DATA['STANDARDS'] = dict()

        col12, col22 = st.columns(2)
        
        with col12:
            PROCEDURE_STANDARDS = pd.DataFrame(list(st.session_state.DB_DATA['STANDARDS'].keys()), columns=["DEVICE TYPE"])
            TBL_STANDARDS, CURRENT_STANDARD = get_selected(PROCEDURE_STANDARDS)

        with col22:
            with st.popover(label=chr(8801)):
                with st.container(border=True):
                    if 'DEVICE_TYPES' not in st.session_state:
                        st.session_state.DEVICE_TYPES = 1
                    device_type = st.selectbox("DEVICE TYPE", options=SQL_SELECT_COLUMN("DEVICE_TYPES", "Id"))
                    if st.button(label='➕ INSERT TYPE', use_container_width=True):
                        if device_type in list(st.session_state.DB_DATA['STANDARDS'].keys()):
                            st.warning(f"< {device_type} > It's already in the list", icon="⚠️")
                        else:
                            st.session_state.DB_DATA['STANDARDS'][device_type] = {}
                            SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
                            st.toast("DATA DB UPDATE")
                            sleep(2)
                            st.rerun()

                if CURRENT_STANDARD and st.button("🗑️ DELETE PROCEDURE", use_container_width=True):
                    @st.experimental_dialog(title="❓")
                    def YESNO_int(info: str):
                        st.text(info)
                        col12, col22 = st.columns(2)
                        with col12:
                            if st.button("YES", use_container_width=True):
                                st.session_state.DB_DATA['SPECIFICATIONS'].pop(CURRENT_PROCEDURE)
                                SQL_UPDATE_DB("PROCEDURES", PROCEDURE_ID, st.session_state.DB_DATA)
                                st.rerun()
                        with col22:
                            if st.button("NO", use_container_width=True):
                                st.rerun()
                    
                    YESNO_int(f"DO YOU WANT TO DELETE THIS STANDARD?\n< {CURRENT_PROCEDURE} >")

        st.text("") # SEPARATOR
        st.markdown(''':blue-background[💊 CMC:]''')

        column_config={
            'RANGE1_MIN': st.column_config.NumberColumn(default=0.0),
            'RANGE1_MAX': st.column_config.NumberColumn(default=0.0),
            'RANGE2_MIN': st.column_config.NumberColumn(default=None),
            'RANGE2_MAX': st.column_config.NumberColumn(default=None),
            'EVALUATION': st.column_config.TextColumn(default="-"),
            'C1': st.column_config.NumberColumn(format="%.2e", default=None), # 0.0
            'C2': st.column_config.NumberColumn(format="%.2e", default=None), # 0.0
            'C3': st.column_config.NumberColumn(format="%.2e", default=None), # 0.0
        }

        DF = pd.DataFrame(columns=list(column_config.keys()))
        TBL_DATA = st.data_editor(
            DF,
            hide_index=True,
            num_rows='dynamic',
            column_config={
                'RANGE1_MIN': st.column_config.NumberColumn(default=0.0),
                'RANGE1_MAX': st.column_config.NumberColumn(default=0.0),
                'RANGE2_MIN': st.column_config.NumberColumn(default=None),
                'RANGE2_MAX': st.column_config.NumberColumn(default=None),
                'EVALUATION': st.column_config.TextColumn(default="-"),
                'C1': st.column_config.NumberColumn(format="%.2e", default=0.0),
                'C2': st.column_config.NumberColumn(format="%.2e", default=0.0),
                'C3': st.column_config.NumberColumn(format="%.2e", default=0.0),
            },
            use_container_width=True
        )

        st.write(CURRENT_PROCEDURE["DB"])

        ## PYDATA
        st.text("")
        st.text("")
        st.subheader('PYDATA:', divider='blue')

        # st.sidebar.markdown("""
        # [➡️ PYDATA](#pydata)
        # """, unsafe_allow_html=True)

        # if WIDGETS.PYDATA.name not in st.session_state:
        #     st.session_state[WIDGETS.PYDATA.name] = ""

        with st.popover(USUAL_ICONS.EXPANDER.value + "  OPTIONS:"):
            ## EDIT TEXT
            if st.button("EDIT PYDATA CODE", use_container_width=True):
                @st.experimental_dialog("EDIT PYDATA CODE", width="large")
                def EDIT_PYDATA():
                    new_code = st.text_area('CODE', value=CURRENT_PROCEDURE["PYDATA"])
                    # if st.button("UPDATE", use_container_width=True):
                    #     st.session_state[WIDGETS.PYDATA.name] = new_code
                    #     st.rerun()
                EDIT_PYDATA()

            ## EDIT BY FILE
            # if "uploaded_file" not in st.session_state:
            #     st.session_state["uploaded_file"] = None

            # uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type='py', key="file_uploader")
            # if uploaded_file is not None:
            #     # To convert to a string based IO:
            #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #     string_data = stringio.read()
            #     st.session_state[WIDGETS.PYDATA.name] = string_data
            #     st.session_state["uploaded_file"] = None

        tx_pydata = st.code(CURRENT_PROCEDURE["PYDATA"], language='python')
