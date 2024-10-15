import os
from menus import *
import streamlit.components.v1 as components


## SESSION STATES
## __________________________________________________________________________________________________

if 'role' not in st.session_state:
    st.session_state.role = None


## PAGE
## __________________________________________________________________________________________________

st.title('SETTINGS PAGE')

# st.logo(os.path.join(path_resources, 'LOGO2.svg'))

with st.expander(':material/home_repair_service: GET DESKTOP APPLICATION'):
    st.download_button(
        ':material/download: DOWNLOAD FLEXICAL DESKTOP', 
        data=os.path.join(path_resources, 'FLEXICAL.txt'),
        file_name='FLEXICAL.txt',
        use_container_width=True
    )
    st.file_uploader('UPLOAD FLEXICAL DESKTOP REQUEST')

st.selectbox(':material/query_stats: KPIs', options=['Last 6 Months', 'Last 12 Months'], index=None)


## UNDER TEST
## __________________________________________________________________________________________________

st.text('\n\n')
st.title('UNDER TEST COMPONENTS')

# if st.button(':material/database: GET DATABASE BACKUP', use_container_width=True):
#     pass


with st.expander('Under test components'):
    # Components Bootstrap
    st.subheader("Integrate Bootstrap")
    components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <div class="card" style="width: 18rem;">
    <img class="card-img-top" src="https://cataas.com/cat?height=200" alt="Card image cap">
    <div class="card-body">
        <h5 class="card-title">A Bootstrap Card</h5>
        <p class="card-text">In Streamlit!</p>
        <a href="https://cataas.com/" class="btn btn-primary">Go to cat API</a>
    </div>
    </div>
    """,
        height=400,
    )

    # STYLE WITH CSS THROUGH MARKDOWN
    if st.checkbox("Make all buttons round", False):
        st.markdown(
            """
        <style>
        .stButton>button {
            border-radius: 50%;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    # STYLE WITH JS THROUGH HTML IFRAME
    st.subheader("Style particular buttons")

    st.button("Hello Red")
    st.button("Hello Blue")
    st.button("Hello Green")

    components.html(
        """
    <script>
    const elements = window.parent.document.querySelectorAll('.stButton button')
    elements[0].style.backgroundColor = 'lightcoral'
    elements[1].style.backgroundColor = 'lightblue'
    elements[2].style.backgroundColor = 'lightgreen'
    </script>
    """,
        height=0,
        width=0,
    )

    if st.selectbox(
        label='THEME',
        options=['light', 'dark']
        ):
        pass

    components.html(
    '''
    <script>
        import Widget from './Widget.svelte';
    </script>

    <div>
        <Widget />
    </div>

    <div class="foo">
        <button disabled>can't touch this</button>
    </div>
    ''')

    # components.html(
    # '''
    # <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    # <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    # <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    # <ul class="nav nav-tabs">
    #     <li role="presentation" class="active"><a href="#">Home</a></li>
    #     <li role="presentation"><a href="#">Profile</a></li>
    #     <li role="presentation"><a href="#">Messages</a></li>
    # </ul>
    # '''
    # )