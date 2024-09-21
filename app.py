import os
import streamlit as st

st.set_page_config(
    page_title="FLEXICAL WEBAPP",
    page_icon='🎛️',
    layout="wide", # "centered",
    initial_sidebar_state= "auto" # "collapsed"
)

from menus import *
from db import *

if "role" not in st.session_state:
    st.session_state.role = None

def logout():
    st.session_state.role = None
    st.rerun()

st.logo(os.path.join(path_resources, r"LOGO2.svg"))

## PAGES
page_home = st.Page(r'navigation/home.py', title="Home", icon=":material/home:", default=(not st.session_state.role))
page_login = st.Page(r'navigation/login.py', title="Log in", icon=":material/login:")
page_logout = st.Page(logout, title="Log out", icon=":material/logout:")
page_settings = st.Page(r"navigation/settings.py", title="Settings", icon=":material/settings:")

page_database = st.Page(
    r"navigation/database.py",
    title="DATABASE",
    icon=':material/database:', #"", 🗄️
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
    icon=':material/procedure:',
    default=(st.session_state.role == ROLES.ADMIN)
)

page_models = st.Page(
    r"navigation/models.py",
    title="MODELS",
    icon=':material/directions_car:', #":material/help:",
    # default=(st.session_state.role == ROLES.TECHNICIAN),
)

page_scopes = st.Page(
    r'navigation/scopes.py',
    title='LAB. SCOPES',
    icon=':material/biotech:',
)

page_templates = st.Page(
    r'navigation/templates.py',
    title='TEMPLATES',
    icon=':material/text_snippet:',
)


## GROUPS
pages_account = [page_logout, page_settings]
pages_technician = [page_database, page_calibrations]
pages_admin = [page_procedures, page_models, page_scopes, page_templates]

## NAVIGATION
pages_dict = {}

st.session_state.role = ROLES.ADMIN

if st.session_state.role in [ROLES.TECHNICIAN, ROLES.ADMIN]:
    pages_dict[ROLES.TECHNICIAN.name] = pages_technician

if st.session_state.role == ROLES.ADMIN:
    pages_dict[ROLES.ADMIN.name] = pages_admin

if len(pages_dict) > 0:
    pg = st.navigation({'': [page_home], "Account": pages_account} | pages_dict)
else:
    # pg = st.navigation([st.Page(login)])
    pg = st.navigation([page_home, page_login])

pg.run()
