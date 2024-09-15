import os
import streamlit as st


# from st_supabase_connection import SupabaseConnection, execute_query
# conn = st.connection("supabase", type=SupabaseConnection, ttl=None)

from menus import *

st.set_page_config(
    page_title="FLEXICAL WEBAPP",
    page_icon='🎛️',
    layout="wide", # "centered",
    initial_sidebar_state= "auto" # "collapsed"
)

if "role" not in st.session_state:
    st.session_state.role = None

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES.list())
    if st.button("Log in"):
        st.session_state.role = ROLES[role]
        st.rerun()

# def login():

#     col13, col23, col33 = st.columns([1,1,1])

#     with col23:
#         st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer
#         st.session_state.role = None
#         USERNAME = st.text_input("USER NAME OR MAIL *")
#         PASSWORD = st.text_input("PASSWORD *", type='password')
#         st.text("") # SEPARATOR
#         BTN = st.button(label="🪪 LOG IN", use_container_width=True)
#         # st.page_link(page='app.py', label="Forgot your password?")

#         if BTN:
#             st.session_state.role = ROLES.ADMIN
#             # if not USERNAME or USERNAME == str():
#             #     INFOBOX("PLEASE pon el nombre bro")
#             # else:
#             #     if "@" in USERNAME:
#             #         SQL = SQL_BY_ROW("USERS", "MAIL", USERNAME)
#             #     else:
#             #         SQL = SQL_BY_ROW("USERS", "Id", USERNAME.upper())
#             #     if len(SQL) == 1:
#             #         USER = SQL[0]["Id"]
#             #         st.session_state.LOGIN_STATUS = USER
#             #     else:
#             #         INFOBOX("INVALID USER/MAIL")
            
#             ## PASSWORD CHECK
#             # if PASSWORD == None or PASSWORD == str():
#                 # INFOBOX(PASSWORD)

#             ## LOGIN
#             # if st.session_state.LOGIN_STATUS:
#             #     sleep(3)
#             #     st.switch_page(r"pages/HOME.py")

def logout():
    st.session_state.role = None
    st.rerun()

## PAGES
page_logout = st.Page(logout, title="Log out", icon=":material/logout:")
page_settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

page_database = st.Page(
    r"navigation/database.py",
    title="DATABASE",
    icon='🗄️', #":material/help:",
    default=(st.session_state.role == ROLES.TECHNICIAN),
)

page_calibrations = st.Page(
    r"navigation/calibrations.py",
    title="CALIBRATIONS",
    icon='🗄️', #":material/help:",
    # default=(st.session_state.role == ROLES.TECHNICIAN),
)

page_procedures = st.Page(
    r'navigation/procedures.py',
    title='PROCEDURES',
    icon='📈',
    default=(st.session_state.role == ROLES.ADMIN)
)

page_scopes = st.Page(
    r'navigation/scopes.py',
    title='LAB. SCOPES',
    icon='📈',
)

page_templates = st.Page(
    r'navigation/templates.py',
    title='TEMPLATES',
    icon='📈',
)


## GROUPS
pages_account = [page_logout, page_settings]
pages_technician = [page_database, page_calibrations]
pages_admin = [page_procedures, page_scopes, page_templates]

## NAVIGATION
pages_dict = {}

if st.session_state.role in [ROLES.TECHNICIAN, ROLES.ADMIN]:
    pages_dict[ROLES.TECHNICIAN.name] = pages_technician

if st.session_state.role == ROLES.ADMIN:
    pages_dict[ROLES.ADMIN.name] = pages_admin

if len(pages_dict) > 0:
    pg = st.navigation({"Account": pages_account} | pages_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
