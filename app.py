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

## PAGES
page_home = st.Page(r'navigation/home.py', title="Home", icon=":material/home:", default=(not st.session_state.role))
page_login = st.Page(r'navigation/login.py', title="Log in", icon=":material/login:")
page_logout = st.Page(logout, title="Log out", icon=":material/logout:")
page_settings = st.Page(r"navigation/settings.py", title="Settings", icon=":material/settings:")

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

# if not st.session_state.role:

if st.session_state.role in [ROLES.TECHNICIAN, ROLES.ADMIN]:
    pages_dict[ROLES.TECHNICIAN.name] = pages_technician

if st.session_state.role == ROLES.ADMIN:
    pages_dict[ROLES.ADMIN.name] = pages_admin

if len(pages_dict) > 0:
    pg = st.navigation({"Account": pages_account} | pages_dict)
else:
    # pg = st.navigation([st.Page(login)])
    pg = st.navigation([page_home, page_login])

pg.run()
