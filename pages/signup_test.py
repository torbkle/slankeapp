import streamlit as st
from supabase_klient import supabase
import re

st.set_page_config(page_title="Registrering", layout="centered")
st.title("🧑‍💻 Opprett ny bruker – Slankeapp")

# 📧 Registreringsskjema
st.subheader("Fyll inn informasjon")
email = st.text_input("E-post")
password = st.text_input("Passord", type="password")
fornavn = st.text_input("Fornavn")
etternavn = st.text_input("Etternavn")
alder = st.number_input("Alder", min_value=0, max_value=120, value=30)

# 📋 Validering
def er_gyldig_epost(epost):
    return re.match(r"[^@]+@[^@]+\.[^@]+", epost)

def er_gyldig_passord(pw):
    return len(pw) >= 8 and any(c.isdigit() for c in pw)

# 🔘 Registreringsknapp
if st.button("Opprett bruker"):
    if not er_gyldig_epost(email):
        st.error("🚫 Ugyldig e-postadresse.")
        st.stop()
    if not er_gyldig_passord(password):
        st.error("🚫 Passordet må være minst 8 tegn og inneholde tall.")
        st.stop()

    try:
        # 🔐 Registrer bruker via Supabase Auth
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        user = auth_response.user

        if not user:
            st.error("🚫 Registrering feilet – ingen bruker returnert.")
            st.stop()

        uid = user.id  # Dette er auth.uid()
        st.success(f"✅ Registrert! Din auth.uid() er:\n`{uid}`")

        # 📥 Lagre brukerprofil i tabellen "brukere"
        st.info("Lagrer brukerprofil i `brukere`...")
        profile = {
            "id": uid,  # Må matche auth.uid() for RLS
            "email": email,
            "fornavn": fornavn,
            "etternavn": etternavn,
            "alder": alder,
            "rolle": "bruker"
        }

        response = supabase.table("brukere").insert(profile).execute()

        if response.status_code == 201:
            st.success("✅ Brukerprofil lagret! RLS-policyen fungerer.")
            st.json(profile)
        else:
            st.error("🚫 RLS-policyen blokkerer innsetting.")
            st.code(response.json(), language="json")

    except Exception as e:
        st.error("🚫 Feil ved registrering.")
        st.code(str(e), language="json")
