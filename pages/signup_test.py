import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Testregistrering", layout="centered")
st.title("🧪 Testregistrering – Slankeapp")

# 1. Registrer testbruker
st.subheader("📧 Opprett testbruker")
email = st.text_input("E-post", value="test@slankeapp.no")
password = st.text_input("Passord", value="Test1234!", type="password")

if st.button("Registrer testbruker"):
    try:
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        uid = auth_response.user.id
        st.success(f"✅ Registrert! Din auth.uid() er:\n`{uid}`")

        # 2. Lagre brukerprofil
        st.info("📥 Lagrer brukerprofil i `brukere`...")
        response = supabase.table("brukere").insert({
            "id": uid,
            "email": email,
            "fornavn": "Test",
            "etternavn": "Bruker",
            "alder": 99,
            "rolle": "debug"
        }).execute()

        if response.status_code == 201:
            st.success("✅ Brukerprofil lagret! RLS-policyen fungerer.")
        else:
            st.error(f"🚫 Feil ved lagring: {response}")
    except Exception as e:
        st.error(f"🚫 Feil ved registrering:\n\n{e}")
