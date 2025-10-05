import streamlit as st
from supabase_klient import supabase
import datetime

st.set_page_config(page_title="Auth Settings Check", layout="centered")
st.title("🔍 Auth Settings Check – Slankeapp")

# 🔍 Sjekk aktiv bruker
user_response = supabase.auth.get_user()
user = user_response.user

if not user:
    st.error("🚫 Du er ikke innlogget – Supabase tolker deg som 'anon'.")
    st.stop()

uid = user.id
email = user.email
st.success(f"✅ Du er innlogget som `{email}`\n`auth.uid()` = `{uid}`")

# 📋 Sjekk bekreftelsesstatus via Supabase systemtabell
try:
    response = supabase.table("auth.users").select("email, confirmed_at").eq("id", uid).execute()
    data = response.data[0]
    bekreftet = data["confirmed_at"]

    if bekreftet:
        st.success(f"📬 E-post er bekreftet: `{bekreftet}`")
    else:
        st.warning("⚠️ E-post er ikke bekreftet – RLS vil blokkere deg.")

        # 🛠️ Valgfritt: Bekreft e-post manuelt (kun for testing)
        if st.button("✅ Bekreft e-post manuelt (test)"):
            nå = datetime.datetime.utcnow().isoformat()
            supabase.table("auth.users").update({"confirmed_at": nå}).eq("id", uid).execute()
            st.success("✅ E-post er nå bekreftet.")
            st.rerun()

except Exception as e:
    st.error("🚫 Klarte ikke hente bekreftelsesstatus.")
    st.code(str(e), language="json")
