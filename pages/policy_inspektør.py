import streamlit as st
from supabase_klient import supabase
import datetime

st.set_page_config(page_title="Policyinspektør", layout="centered")
st.title("🔐 RLS Policyinspektør – brukere")

# 🔐 Sjekk aktiv sesjon
session = supabase.auth.get_session()
user = supabase.auth.get_user().user if session else None

if not user:
    st.error("🚫 Ingen aktiv sesjon – logg inn først.")
    st.stop()

st.success(f"✅ Innlogget som `{user.email}`")
st.write(f"🔑 auth.uid(): `{user.id}`")

# 📬 Sjekk om e-post er bekreftet
if user.email_confirmed_at:
    st.info(f"📬 E-post bekreftet: `{user.email_confirmed_at}`")
else:
    st.warning("⚠️ E-post ikke bekreftet – RLS vil blokkere innsetting.")

# 🧪 Testinnsetting i `brukere`
st.subheader("📥 Tester innsetting i `brukere`")

test_data = {
    "id": user.id,
    "email": user.email,
    "fornavn": "Policy",
    "etternavn": "Test",
    "alder": 99,
    "rolle": "bruker",
    "opprettet": datetime.datetime.utcnow().isoformat()
}

response = supabase.table("brukere").insert(test_data).execute()

if response.status_code == 201:
    st.success("✅ RLS-policy godtar innsetting.")
    st.json(test_data)
else:
    st.error("🚫 RLS-policy blokkerer innsetting.")
    st.code(response.json())
