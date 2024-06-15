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
from menu import USUAL_ICONS, SSTATE, GET_FIRM, path_resources, SIDEBAR
from db import conn, execute_query, SQL_PROCEDURES, SQL_INSERT, SQL_ID_COUNT, SQL_SELECT_COLUMN



## SESSION STATES
## __________________________________________________________________________________________________

if not st.session_state[SSTATE.LOGIN_STATUS]:
    st.switch_page(r"pages/PROFILE.py")

# if SSTATE.LOGIN_STATUS not in st.session_state:
#     st.session_state[SSTATE.LOGIN_STATUS] = None

if SSTATE.PROCEDURES_COUNT not in st.session_state:
    st.session_state[SSTATE.PROCEDURES_COUNT] = 1

if 'DB_DATA' not in st.session_state:
    st.session_state.DB_DATA = None


## MENU
## __________________________________________________________________________________________________

class PROCEDURE:

    class TypeDict(TypedDict):
        Id: str
        TITLE: str
        INFO: str
        DB: dict
        PYDATA: str
        FIRM: str

@st.experimental_dialog("NEW PROCEDURE FORM")
def FORM_NEWPROCEDURE():
    ID = st.text_input("Id *")
    TITLE = st.text_input("DEFALUT TEST TITLE *")
    INFO = st.text_area("INFO")

    if st.button(label="💽 CREATE NEW PROCEDURE", use_container_width=True):
        CHECK: bool = True
        if CHECK and (not ID or not TITLE or not INFO):
            st.warning(f"Complete all * fields", icon=USUAL_ICONS.WARNINNG.value)
            CHECK = False
        if SQL_ID_COUNT("PROCEDURES", ID):
            st.warning(f"< {ID} > is already in the DATABASE", icon="🚨")
            CHECK = False
        if CHECK:
            ## INSERT
            VALUES = {
                "Id": ID.upper(), 
                "TITLE": TITLE.upper(),
                "INFO": INFO,
                "FIRM": GET_FIRM()
            }
            SQL_INSERT("PROCEDURES", VALUES)
            st.session_state[SSTATE.PROCEDURES_COUNT] += 1
            st.info("New Procedure Added !!", icon='🏁')
            sleep(3)
            st.rerun()

@st.cache_resource
def SQL_PROCEDURE(PROCEDURE_ID: str, COUNT: int):
    print(f"SQL MODEL DATA ({COUNT}):", GET_FIRM())
    return execute_query(conn.table('PROCEDURES').select('*', count='exact').like("Id", PROCEDURE_ID))


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
st.sidebar.divider()
st.sidebar.page_link("app.py", label="HOME", icon="🏠")
if st.session_state[SSTATE.LOGIN_STATUS]:
    st.sidebar.page_link(r"pages/DEVICE_TYPES.py", label="DEVICE TYPES", icon="🚗")
    st.sidebar.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗")



## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"procedures.svg"), use_column_width=False)
st.divider()

tab_db, tab_editor = st.tabs(["📒 DATABASE", "✏️ EDITOR"])


## DATABASE
## __________________________________________________________________________________________________

with tab_db:

    if st.session_state[SSTATE.LOGIN_STATUS]:
        if st.button("💾 CREATE NEW PROCEDURE", use_container_width=True): # or sd_btn_new:
            FORM_NEWPROCEDURE()


    if st.session_state[SSTATE.LOGIN_STATUS]:

        st.text("") # SEPARATOR
        st.text("") # SEPARATOR
        st.subheader('DATABASE:', divider='blue')

        # st.sidebar.markdown("""
        # [➡️ DATABASE](#database)
        # """, unsafe_allow_html=True)

        placeholder = st.empty()
        if placeholder.button("🧬 LOAD DATABASE", use_container_width=True):
            with placeholder.expander("🧬 DATABASE", expanded=True):
                SQL = SQL_PROCEDURES(st.session_state[SSTATE.PROCEDURES_COUNT])
                DATAFRAME = pd.DataFrame(SQL)
                del DATAFRAME["DB"]
                del DATAFRAME["PYDATA"]
                st.dataframe(
                    # data=pd.DataFrame(SQL),
                    data=DATAFRAME,
                    use_container_width=True,
                    hide_index=True
                )


## EDITOR
## __________________________________________________________________________________________________

with tab_editor:

    col12, col22 = st.columns(2)

    with col12:
        print(SQL_PROCEDURES(1))
        PROCEDURE_ID = st.selectbox("🎛️ PROCEDURE Id", options=[procedure['Id'] for procedure in SQL_PROCEDURES(st.session_state[SSTATE.PROCEDURES_COUNT])], index=None)

    if PROCEDURE_ID:
        SQL = SQL_PROCEDURE(PROCEDURE_ID, st.session_state[SSTATE.PROCEDURES_COUNT])

        if SQL.count != 1:
            st.session_state.DB_DATA = None
            st.warning(f"< {PROCEDURE_ID} > don't exits", icon="⚠️")

        else:
            CURRENT_PROCEDURE = PROCEDURE.TypeDict(**SQL.data[0])

            ## DATA
            st.text("")
            st.text("")
            st.subheader('DATA:', divider='blue')

            tx_title = st.text_input(label='DEFAULT TEST TITLE', value=CURRENT_PROCEDURE["TITLE"])
            tx_info = st.text_input(label='INFO', value=CURRENT_PROCEDURE["INFO"])


            ## REPORT FORMATS
            st.text("")
            st.text("")
            st.subheader('REPORT FORMATS:', divider='blue')

            st.text("") # SEPARATOR
            st.markdown(''':blue-background[💊 REPORT FORMATS:]''')

            st.text("") # SEPARATOR
            st.markdown(''':blue-background[💊 STANDARDS:]''')

            col12, col22 = st.columns(2)
            
            with col12:
                edited_df = st.data_editor(
                    pd.DataFrame(columns=["✔️", 'DEVICE TYPE']),
                    hide_index=True,
                    column_config={
                        "✔️": st.column_config.CheckboxColumn(required=True, width='small'),
                        'DEVICE TYPE': st.column_config.TextColumn(required=True, width='large'),
                    },
                    # disabled=DATAFRAME.columns,
                    use_container_width=True
                )

            with col22:
                st.popover(label=chr(8801))

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
