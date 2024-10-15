import os
from menus import *
from db import *



## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None

if 'CALIBRATIONS' not in st.session_state:
    st.session_state.CALIBRATIONS = 1


## TOOLS
## __________________________________________________________________________________________________



## PAGE
## __________________________________________________________________________________________________

# st.logo(os.path.join(path_resources, 'LOGO2.svg'))
st.title('CALIBRATIONS PAGE')
st.markdown('---')

with st.expander(':material/publish: IMPORT CALIBRATIONS'):
    st.file_uploader(
        label='JSON FILE',
        type=['json'],
        accept_multiple_files=True
    )

# st.selectbox('')

st.text('SEARCH CALIBRATION')
with st.expander(':material/filter_list: FILTERS'):

    st.text_input('CALIBRATION Id:')
    st.text_input('DEVICE Id:')


st.text('SEARCH CALIBRATION BY EVENT')
EVENTS = ['ONSITE CAMPAIGN', 'REPAIR', 'EXT. CALIBRATION']
cb_event = st.selectbox(
    label='EVENT',
    options=EVENTS,
    index=None,
    label_visibility='collapsed'
)

if cb_event == EVENTS[0]:
    st.write(EVENTS[0])
if cb_event == EVENTS[1]:
    st.write(EVENTS[1])
if cb_event == EVENTS[2]:
    st.write(EVENTS[2])



# with st.expander(':material/filter_list: FILTERS'):
#     st.text_input('ONSITE CAMPAIGN:')
#     st.text_input('SEND TO CALIBRATE:')



## UNDER TEST
## __________________________________________________________________________________________________


st.markdown('---')


st.write(':material/warning: UNDER CONSTRUCTION')
t = '''
In this page, depends of the user profile show diferent views:
- Admin:
    - All calibrations
    - Stadistics
    - Editors
- Technician:
    - Asigned calibrations
    - Onsite campaings
    - Asigned Projects
'''
st.caption(t)

