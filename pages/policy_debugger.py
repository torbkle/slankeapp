import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Policy Debugger", layout="centered")
st.title("🔐 Policy Debugger – Brukere-tabellen")

def hent_policies():
    query = """
    SELECT policyname, cmd, roles, qual, check
    FROM pg_policies
    WHERE tablename = 'brukere';
    """
    return supabase.rpc("execute_sql", {"sql": query}).data

def vis_policies():
    st.subheader("📋 Aktive RLS-policyer")
    policies = hent_policies()
    if not policies:
        st.warning("Ingen policyer funnet.")
        return
    for p in policies:
        st.markdown(f"**{p['policyname']}** – `{p['cmd']}` for `{p['roles']}`")
        st.code(f"USING: {p['qual']}\nWITH CHECK: {p['check']}")

def test_auth_uid():
    try:
        user = supabase.auth.get_user()
        uid = user.user.id
        st.success(f"✅ Du er autentisert. Din auth.uid() er:\n`{uid}`")
        return uid
    except Exception as e:
        st.error("🚫 Du er ikke autentisert. RLS vil blokkere innsetting.")
        return None

def opprett_policy():
    sql = """
    DROP POLICY IF EXISTS "Tillat registrering av ny bruker" ON public.brukere;
    CREATE POLICY "Tillat registrering av ny bruker"
    ON public.brukere
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = id);
    """
    try:
        supabase.rpc("execute_sql", {"sql": sql})
        st.success("✅ Policy opprettet eller oppdatert.")
    except Exception as e:
        st.error(f"Feil ved oppretting: {e}")

vis_policies()
uid = test_auth_uid()

if st.button("🔄 Opprett eller oppdater policy"):
    opprett_policy()
