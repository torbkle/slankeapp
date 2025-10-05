import streamlit as st
from supabase_klient import supabase

def login_form():
    st.sidebar.header("🔐 Logg inn")
    email = st.sidebar.text_input("E-post")
    password = st.sidebar.text_input("Passord", type="password")

    if st.sidebar.button("Logg inn"):
        try:
            response = supabase.table("brukere")\
                .select("id, fornavn, etternavn, rolle")\
                .eq("email", email)\
                .eq("passord", password)\
                .execute()

            if response.data:
                bruker = response.data[0]
                st.session_state["innlogget"] = True
                st.session_state["bruker_id"] = bruker["id"]
                st.session_state["navn"] = bruker["fornavn"]
                st.session_state["email"] = email
                st.session_state["rolle"] = bruker.get("rolle", "bruker")
                st.success(f"✅ Velkommen, {bruker['fornavn']}!")
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

    if st.sidebar.button("Registrer"):
        if not (fornavn and etternavn and email and passord):
            st.error("Alle felt må fylles ut.")
            return
        try:
            eksisterende = supabase.table("brukere").select("id").eq("email", email).execute()
            if eksisterende.data:
                st.warning("E-postadressen er allerede registrert.")
                return

            supabase.table("brukere").insert({
                "fornavn": fornavn.strip(),
                "etternavn": etternavn.strip(),
                "alder": int(alder),
                "email": email.strip().lower(),
                "passord": passord,
                "rolle": "bruker"
            }).execute()
            st.success("✅ Bruker opprettet! Du kan nå logge inn.")
        except Exception as e:
            st.error(f"Feil ved registrering: {e}")

def logg_ut_knapp():
    if st.sidebar.button("Logg ut"):
        st.session_state.clear()
        st.success("Du er logget ut.")

def krever_innlogging():
    if "innlogget" not in st.session_state or not st.session_state["innlogget"]:
        st.warning("Du må logge inn for å bruke appen.")
        st.stop()

def er_admin():
    return st.session_state.get("rolle") == "admin"
