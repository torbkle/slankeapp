import streamlit as st

def login():
    st.sidebar.header("🔐 Logg inn")
    username = st.sidebar.text_input("Brukernavn")
    password = st.sidebar.text_input("Passord", type="password")

    if st.sidebar.button("Logg inn"):
        if username == "demo" and password == "slank123":
            st.session_state["innlogget"] = True
            st.success("✅ Innlogging vellykket")
        else:
            st.error("Feil brukernavn eller passord")

def krever_innlogging():
    if "innlogget" not in st.session_state or not st.session_state["innlogget"]:
        st.warning("Du må logge inn for å bruke appen.")
        st.stop()
