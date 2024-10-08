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
st.write('UNDER CONSTRUCTION')
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