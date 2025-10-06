import streamlit as st
from supabase_klient import supabase
from bekreft_epost import bekreft_epost
import datetime

st.set_page_config(page_title="Auth Test", layout="centered")
st.title("🧪 Supabase Auth Test")

email = st.text_input("E-post").strip()
password = st.text_input("Passord", type="password")

if st.button("Registrer og test"):
    try:
        # 🔐 Registrer bruker
        signup_response = supabase.auth.sign_up({"email": email, "password": password})
        user = signup_response.user

        if not user:
            st.error("🚫 Registrering feilet – ingen bruker returnert.")
            st.stop()

        uid = user.id
        st.success(f"✅ Registrert! auth.uid(): `{uid}`")

        # 📬 Bekreft e-post via Admin API
        bekreft_response = bekreft_epost(uid)
        if bekreft_response.status_code == 200:
            st.info("📬 E-post bekreftet via Admin API.")
        else:
            st.warning("⚠️ Klarte ikke bekrefte e-post.")
            st.code(bekreft_response.text)

        # 🔁 Tving ny innlogging
        supabase.auth.sign_out()
        login_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = login_response.user
        session = login_response.session

        if not user:
            st.error("🚫 Innlogging feilet – ingen bruker returnert.")
            st.stop()

        st.success(f"✅ Innlogget som `{user.email}`")
        st.write(f"auth.uid(): `{user.id}`")

        # 📬 E-poststatus
        if user.email_confirmed_at:
            st.info(f"📬 E-post bekreftet: `{user.email_confirmed_at}`")
        else:
            st.warning("⚠️ E-post ikke bekreftet – RLS vil sannsynligvis blokkere deg.")

        # 🔑 Tokens
        st.subheader("🔑 Tokens")
        st.code(session.access_token, language="text")

        # 🧪 Sjekk aktiv sesjon
        session_check = supabase.auth.get_user()
        if session_check and session_check.user:
            st.success("✅ Aktiv sesjon bekreftet.")
        else:
            st.error("🚫 Ingen aktiv sesjon – du er ikke authenticated.")

    except Exception as e:
        st.error("🚫 Feil under Auth-flyten.")
        st.code(str(e))
