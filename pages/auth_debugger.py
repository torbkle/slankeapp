import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Auth Debugger", layout="centered")
st.title("🛡️ Auth Debugger – Slankeapp")

# 🔍 Sjekk aktiv bruker
user_response = supabase.auth.get_user()
user = user_response.user

if user:
    uid = user.id
    st.success(f"✅ Du er innlogget som authenticated bruker.\n`auth.uid()` = `{uid}`")
else:
    st.error("🚫 Du er ikke innlogget – Supabase tolker deg som 'anon'.")
    st.stop()

# 🧪 Test innsetting i `brukere`
st.subheader("Test RLS-policy for `brukere`")
if st.button("Test innsetting"):
    test_profile = {
        "id": uid,
        "email": "debug@slankeapp.no",
        "fornavn": "Debug",
        "etternavn": "Bruker",
        "alder": 99,
        "rolle": "debug"
    }

    response = supabase.table("brukere").insert(test_profile).execute()

    if response.status_code == 201:
        st.success("✅ RLS-policyen godtar innsetting.")
        st.json(test_profile)
    else:
        st.error("🚫 RLS-policyen blokkerer innsetting.")
        st.code(response.json(), language="json")
