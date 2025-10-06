import streamlit as st
from supabase_klient import supabase
import datetime

st.set_page_config(page_title="RLS Debugger", layout="centered")
st.title("🔐 RLS Debugger – Slankeapp")

email = st.text_input("E-post").strip()
password = st.text_input("Passord", type="password")

if st.button("Test RLS-innsetting"):
    # 🔐 Logg inn
    try:
        login_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = login_response.user
        st.success(f"✅ Innlogget som: {user.email}")
    except Exception as e:
        st.error("🚫 Innlogging feilet – Supabase Auth kastet en feil.")
        st.code(str(e))
        st.stop()

    user = login_response.user

    if not user:
        st.error("🚫 Innlogging feilet – ingen bruker returnert.")
        st.stop()

    uid = user.id
    st.success(f"✅ Innlogget som `{user.email}`")
    st.write(f"auth.uid(): `{uid}`")

    # 📬 Sjekk e-poststatus
    if user.email_confirmed_at:
        st.info(f"📬 E-post bekreftet: `{user.email_confirmed_at}`")
    else:
        st.warning("⚠️ E-post ikke bekreftet – RLS vil sannsynligvis blokkere innsetting.")

    # 🧪 Testinnsetting i `brukere`
    test_data = {
        "id": uid,
        "email": user.email,
        "fornavn": "Test",
        "etternavn": "Bruker",
        "alder": 42,
        "rolle": "bruker",
        "opprettet": datetime.datetime.utcnow().isoformat()
    }

    response = supabase.table("brukere").insert(test_data).execute()

    if response.status_code == 201:
        st.success("✅ Innsetting OK – RLS-policyen godtar deg.")
        st.json(test_data)
    else:
        st.error("🚫 Innsetting feilet – RLS blokkerer.")
        st.code(response.json())
