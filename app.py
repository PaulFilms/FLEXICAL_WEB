'''
FLEXICAL v3 | MAIN

streamlit run app.py

'''

## PYTHON LIBRARIES
import os

## IMPORTED LIBRARIES
import streamlit as st

## INTERNAL
from menu import path_resources, SSTATE, SIDEBAR, SB_EDITORS, USUAL_ICONS

st.set_page_config(
    page_title="FLEXICAL DEVELOPER",
    page_icon=":guardsman:",
    layout="wide", # "centered",
    initial_sidebar_state= "auto" # "collapsed"
)


## SESSION STATES
## __________________________________________________________________________________________________

if SSTATE.LOGIN_STATUS not in st.session_state:
    st.session_state[SSTATE.LOGIN_STATUS] = None


## SIDEBAR
## __________________________________________________________________________________________________

SIDEBAR()
if st.session_state[SSTATE.LOGIN_STATUS]:
    # st.sidebar.page_link(r"pages/DATABASE.py", label="DATABASE", use_container_width=True) # , icon="🧬" / ":blue-background[DATABASE]"
    if st.sidebar.button(label="DATABASE", use_container_width=True):
        st.switch_page(r"pages/DATABASE.py")
    SB_EDITORS()




## PAGE
## __________________________________________________________________________________________________

st.logo(os.path.join(path_resources, r"LOGO2.svg"))
st.image(os.path.join(path_resources, r"LOGO2.svg"), use_column_width=False) # flexical_developer
# st.divider()

st.text("ABOUT FLEXICAL")
with st.container(border=True):
    st.caption('''This is a beta version of web application for FLEXICAL''')
    st.caption('''Any functionality may not run a well''')
    st.caption('''In case of troubles, please contact with: ppp@ppp.com''')
    st.markdown('''
    Esta vaina esta pensada para poder añadir varias lineas de texto con formato chimba y se ajuste automaticamente al ancho de la web.\n
    Si no te mola, puedes ponerte en contacto con mi escroto
    ''')

st.text("")
col12, col22 = st.columns(2)

with col12:
    st.write(":blue-background[📒 PAGES]")
    with st.container(border=False):
        st.page_link(r"pages/DATABASE.py", label="DATABASE", use_container_width=True) # icon="🧬", 
        with st.expander(USUAL_ICONS.EXPANDER.value + "  EDITORS", expanded=False):
            st.page_link(r"pages/MODELS.py", label="MODELS", icon="🚗", use_container_width=True)
            st.page_link(r"pages/PROCEDURES.py", label="PROCEDURES", icon="🧬", use_container_width=True)

with col22:
    st.write(":blue-background[🧷 DOCUMENTATION]")
    with st.container(border=False):
        st.page_link("https://pablopila.notion.site/FLEXICAL-cb070d967f6b4f46829a349731095be5?pvs=4", label="NOTION WEB PAGE", use_container_width=True)
        st.page_link("https://github.com/PaulFilms/FLEXICAL_WEB", label="GITHUB REPOSITORY", use_container_width=True)
        st.text(" * SPECIFICATIONS")
        st.text(" * USER MANUAL")
        # st.text("")
        # st.text("")
        # st.text("")
        # st.text("")
        # st.text("")
        # st.text("")

# st.image(r"https://file.notion.so/f/f/21f0811a-a634-472d-8c7b-9a0052fd6b63/969d0671-e768-4a4d-b328-a5f8f0361054/Untitled.png?id=f15b711f-5207-4f97-b551-48c5fbe36521&table=block&spaceId=21f0811a-a634-472d-8c7b-9a0052fd6b63&expirationTimestamp=1718373600000&signature=-f23vCxQFa0Zn8FS-s_tKV0bkpBJTw9jEN1QnrmxQ4g&downloadName=Untitled.png")

st.divider()
# st.text("DEVELOPED FOR R&S TO R&S")
st.image(os.path.join(path_resources, r"R&S Logo - Complete.svg"), 
    # use_column_width=True,
    width=250
)