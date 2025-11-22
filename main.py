import streamlit as st

home_page = st.Page(
    "home.py",
    title="Home",
)
tecoloco_page = st.Page("tecoloco.py", title="Tecoloco")
encuentra24_page = st.Page("encuentra24.py", title="Encuentra24")
computrabajo_page = st.Page("computrabajo.py", title="Computrabajo")

pg = st.navigation(
    [
        home_page,
        tecoloco_page,
        encuentra24_page,
        computrabajo_page,
    ]
)

pg.run()
