import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Testregistrering", layout="centered")
st.title("🧪 Testregistrering – Slankeapp")

# 📧 Registreringsskjema
st.subheader("Opprett testbruker")
email = st.text_input("E-post", value="test@slankeapp.no")
password = st.text_input("Passord", value="Test1234!", type="password")

if st.button("Registrer testbruker"):
    try:
        # 🔐 Registrer bruker via Supabase Auth
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        user = auth_response.user

        if not user:
            st.error("🚫 Registrering feilet – ingen bruker returnert.")
            st.stop()

        uid = user.id
        st.success(f"✅ Registrert! Din auth.uid() er:\n`{uid}`")

        # 📥 Lagre brukerprofil i tabellen "brukere"
        st.info("Lagrer brukerprofil i `brukere`...")
        profile = {
            "id": uid,  # Må matche auth.uid() for RLS
            "email": email,
            "fornavn": "Test",
            "etternavn": "Bruker",
            "alder": 99,
            "rolle": "debug"
        }

        response = supabase.table("brukere").insert(profile).execute()

        if response.status_code == 201:
            st.success("✅ Brukerprofil lagret! RLS-policyen fungerer.")
            st.json(profile)
        else:
            st.error("🚫 Feil ved lagring. RLS-policyen blokkerer innsetting.")
            st.code(response.json(), language="json")

    except Exception as e:
        st.error("🚫 Feil ved registrering.")
        st.code(str(e), language="json")
