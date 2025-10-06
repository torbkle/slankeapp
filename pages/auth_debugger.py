import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Auth Debugger", layout="centered")
st.title("🔍 Supabase Auth Debugger")

email = st.text_input("E-post").strip()
password = st.text_input("Passord", type="password")

if st.button("Test innlogging og sesjon"):
    try:
        # 🔐 Logg inn
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
        st.error("🚫 Supabase Auth kastet en feil.")
        st.code(str(e))
