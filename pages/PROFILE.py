'''
FLEXICAL v3 | PROFILE

'''

## PYTHON LIBRARIES
import os, random
from time import sleep

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



## PAGE
## __________________________________________________________________________________________________

# if not st.session_state.LOGIN_STATUS:
#     st.switch_page(r"pages/LOGIN.py")

## SIDEBAR & BASIC COMPONENTS
# st.logo(os.path.join(path_resources, r"LOGO2.svg"))
SIDEBAR()

# col13, col23, col33 = st.columns(3)

# with col33:
#     if st.button(f"🌐 {st.session_state[SSTATE.LOGIN_STATUS]}  [Log out]", use_container_width=True):
#         st.session_state[SSTATE.LOGIN_STATUS] = None

with st.container(border=True):
    st.caption("This is your Profile page.")
    st.caption("In the next upddates, will you check your data")

# st.divider()

col12, col22 = st.columns(2)

with col12:

    if st.session_state.LOGIN_STATUS:
        with st.expander(USUAL_ICONS.EXPANDER.value + "   OPTIONS", expanded=True):
            text_contents = '''This is some text'''
            st.download_button(USUAL_ICONS.SAVE.value + " DOWNLOAD DESKTOP APP", text_contents, use_container_width=True)
            # st.download_button(USUAL_ICONS.SAVE.value + " DOWNLOAD DATABASE", text_contents, use_container_width=True)

            ## GET LOCAL DATABASE
            holder = st.empty()
            if holder.button("GET DATABASE", use_container_width=True):
                with st.spinner("Generating SQLite database..."):
                    GET_LOCAL_DB()
                
                holder.download_button(
                    label="📩 DOWNLOAD DATABASE",
                    data=open("flexical.db", "rb").read(),
                    file_name="flexical.db",
                    mime="application/x-sqlite3",
                    use_container_width=True
                )
                os.remove("flexical.db")

with col22:
    st.text("Get support:")
    prompt = st.chat_input("Any Question or support??")
    if prompt:
        st.write(f"User has sent the following prompt:")
        st.write(f" -> {prompt}")



st.subheader('STADISTICS:', divider='blue')

col12, col22 = st.columns(2)

with col12:
    SQL = SQL_SELECT_COLUMN("DEVICE_TYPES", "Id")
    # st.write(SQL)
    # print(SQL)
    d = {
        "DEVICE TYPE": [type for type in SQL],
        "Nº OF CALIBRATIONS": [random.randint(1, 100) for type in SQL]
    }
    st.dataframe(
        data=pd.DataFrame(d),
        use_container_width=True,
        hide_index=True,
        column_config={
            "DEVICE TYPE": st.column_config.TextColumn(),
            "Nº OF CALIBRATIONS": st.column_config.ProgressColumn()
        }
    )

with col22:
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)

    size = 0.3
    vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

    cmap = plt.colormaps["tab20c"]
    outer_colors = cmap(np.arange(3)*4)
    inner_colors = cmap([1, 2, 5, 6, 9, 10])

    ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
        wedgeprops=dict(width=size, edgecolor='w'))

    ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
        wedgeprops=dict(width=size, edgecolor='w'))

    # ax.set(
    #     aspect="equal", 
    #     title='Pie plot with `ax.pie`',
    #     # color_cycle="white"
    #     # color='blue'
    # )
    ax.set_title('CALIBRATIONS BY DEVICE TYPE', fontsize=10, color= 'white', fontweight='bold');
    # plt.show()

    st.pyplot(fig)
