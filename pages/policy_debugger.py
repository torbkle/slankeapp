import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Policy Debugger", layout="centered")
st.title("🔐 Policy Debugger – RLS for brukere")

# 1. Test autentisering
def hent_auth_uid():
    try:
        user = supabase.auth.get_user().user
        uid = user.id
        st.success(f"✅ Du er autentisert. Din auth.uid() er:\n`{uid}`")
        return uid
    except Exception:
        st.error("🚫 Du er ikke autentisert. RLS vil blokkere registrering.")
        return None

# 2. Test om policyen fungerer
def test_policy(uid):
    if not uid:
        return
    try:
        response = supabase.table("brukere").insert({
            "id": uid,
            "email": "test@debugger.no",
            "fornavn": "Test",
            "etternavn": "Bruker",
            "alder": 99,
            "rolle": "debug"
        }).execute()
        st.success("✅ Policy fungerer! Du kan registrere ny bruker.")
    except Exception as e:
        st.error(f"🚫 Policy blokkerer registrering:\n\n{e}")

# 3. Opprett policy manuelt
def opprett_policy():
    st.warning("🛠️ Du må kjøre følgende SQL manuelt i Supabase SQL Editor:")
    st.code("""
DROP POLICY IF EXISTS "Tillat registrering av ny bruker" ON public.brukere;

CREATE POLICY "Tillat registrering av ny bruker"
  ON public.brukere
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);
""", language="sql")

# 4. Kjør testene
uid = hent_auth_uid()
if st.button("🚦 Test policy mot auth.uid()"):
    test_policy(uid)

st.divider()
st.subheader("🔧 Opprett policy manuelt")
opprett_policy()
