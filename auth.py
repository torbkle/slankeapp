import streamlit as st
from supabase_klient import supabase
from supabase import create_client

def signup_form():
    st.sidebar.header("🆕 Opprett konto")
    email = st.sidebar.text_input("E-post")
    password = st.sidebar.text_input("Passord", type="password")
    fornavn = st.sidebar.text_input("Fornavn")
    etternavn = st.sidebar.text_input("Etternavn")
    alder = st.sidebar.number_input("Alder", min_value=10, max_value=120)

    if st.sidebar.button("Registrer"):
        try:
            auth_response = supabase.auth.sign_up({"email": email, "password": password})
            uid = auth_response.user.id
            supabase.table("brukere").insert({
                "id": uid,
                "email": email,
                "fornavn": fornavn,
                "etternavn": etternavn,
                "alder": alder,
                "rolle": "bruker"
            }).execute()
            st.success("✅ Konto opprettet! Sjekk e-post for bekreftelse.")
        except Exception as e:
            st.error(f"Feil ved registrering: {e}")

def login_form():
    st.sidebar.header("🔐 Logg inn")
    email = st.sidebar.text_input("E-post")
    password = st.sidebar.text_input("Passord", type="password")

    if st.sidebar.button("Logg inn"):
        try:
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            user = auth_response.user
            uid = user.id
            st.session_state["innlogget"] = True
            st.session_state["bruker_id"] = uid
            st.session_state["email"] = email

            # Hent profil
            profile = supabase.table("brukere").select("fornavn, rolle").eq("id", uid).execute().data[0]
            st.session_state["navn"] = profile["fornavn"]
            st.session_state["rolle"] = profile.get("rolle", "bruker")
            st.success(f"✅ Velkommen, {profile['fornavn']}!")
        except Exception as e:
            st.error(f"Innloggingsfeil: {e}")

def logg_ut_knapp():
    if st.sidebar.button("Logg ut"):
        supabase.auth.sign_out()
        st.session_state.clear()
        st.success("Du er logget ut.")

def krever_innlogging():
    if "innlogget" not in st.session_state or not st.session_state["innlogget"]:
        st.warning("Du må logge inn for å bruke appen.")
        st.stop()

def er_admin():
    return st.session_state.get("rolle") == "admin"
