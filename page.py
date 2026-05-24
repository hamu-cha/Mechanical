import streamlit as st

pg = st.navigation([
    st.Page("pages/TopPage.py", title="00 トップページ"),
    st.Page("pages/Palabola.py", title="01 放物運動"),
    st.Page("pages/CircleMotion.py", title="02 等速円運動"),
    ])

pg.run()