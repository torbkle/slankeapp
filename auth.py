import streamlit as st
from supabase_klient import supabase

def login_form():
    st.sidebar.header("🔐 Logg inn")
    email = st.sidebar.text_input("E-post")
    password = st.sidebar.text_input("Passord", type="password")

    if st.sidebar.button("Logg inn"):
        try:
            response = supabase.table("brukere")\
                .select("id, fornavn, etternavn")\
                .eq("email", email)\
                .eq("passord", password)\
                .execute()
            if response.data:
                st.session_state["innlogget"] = True
                st.session_state["bruker_id"] = response.data[0]["id"]
                st.session_state["navn"] = response.data[0]["fornavn"]
                st.success(f"✅ Velkommen, {response.data[0]['fornavn']}!")
            else:
                st.error("Feil e-post eller passord.")
        except Exception as e:
            st.error(f"Innloggingsfeil: {e}")

def registrer_ny_bruker():
    st.sidebar.header("🆕 Opprett ny bruker")
    fornavn = st.sidebar.text_input("Fornavn")
    etternavn = st.sidebar.text_input("Etternavn")
    alder = st.sidebar.number_input("Alder", min_value=10, max_value=120, step=1)
    email = st.sidebar.text_input("E-postadresse")
    passord = st.sidebar.text_input("Velg passord", type="password")

    if st.sidebar.button("Registr
