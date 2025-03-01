import streamlit as st
import extra_streamlit_components as stx
from dotenv import load_dotenv
import os

load_dotenv()

st.subheader("Ofertas de empleo Nicaragua")
st.write(
    "Aplicación Web que extrae ofertas laborales en Nicaragua de los sitios web: encuentra24, computrabajo y tecoloco"
)
st.write(
    "Desarrollado con fines educativos con Python, Beautifulsoup y Streamlit, la carga puedo tomar algunos segundos para evitar Ban"
)

cookie_manager = stx.CookieManager()

if cookie_manager.get("auth"):
    if st.button("Logout"):
        cookie_manager.delete("auth")
        st.success("Logout successful")

placeholder = st.empty()

current_email = os.getenv("USERNAME")
current_password = os.getenv("PASSWORD")

with placeholder.form("login"):
    st.markdown("#### Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and email == current_email and password == current_password:
    placeholder.empty()
    st.success("Login successful")
    cookie_manager.set("auth", True)
elif submit and email != current_email and password != current_password:
    st.error("Login failed")
    cookie_manager.set("auth", False)
else:
    pass
