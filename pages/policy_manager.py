import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Policy Manager", layout="wide")
st.title("🔐 Policy Manager – RLS-kontroll")

# 📋 Tabeller du vil administrere
tabeller = ["brukere", "vektlogg", "måltider"]
valgt_tabell = st.selectbox("Velg tabell", tabeller)

# 🔍 Hent policyer
def hent_policyer(tabellnavn):
    query = f"SELECT * FROM pg_policies WHERE tablename = '{tabellnavn}';"
    return supabase.rpc("execute_sql", {"sql": query}).data

# 🗑️ Slett policy
def slett_policy(tabell, navn):
    sql = f'DROP POLICY IF EXISTS "{navn}" ON public.{tabell};'
    supabase.rpc("execute_sql", {"sql": sql})

# 🛠️ Opprett anbefalte policyer
def opprett_standard_policy(tabell):
    if tabell == "brukere":
        sql = """
        CREATE POLICY "Tillat registrering av ny bruker"
        ON public.brukere
        FOR INSERT TO authenticated
        WITH CHECK (auth.uid() = id);

        CREATE POLICY "Bruker kan lese egen profil"
        ON public.brukere
        FOR SELECT TO authenticated
        USING (auth.uid() = id);

        CREATE POLICY "Bruker kan oppdatere egen profil"
        ON public.brukere
        FOR UPDATE TO authenticated
        USING (auth.uid() = id);
        """
    else:
        sql = f"""
        CREATE POLICY "Bruker kan lese egne data"
        ON public.{tabell}
        FOR SELECT TO authenticated
        USING (auth.uid() = bruker_id);

        CREATE POLICY "Bruker kan skrive egne data"
        ON public.{tabell}
        FOR INSERT TO authenticated
        WITH CHECK (auth.uid() = bruker_id);

        CREATE POLICY "Bruker kan oppdatere egne data"
        ON public.{tabell}
        FOR UPDATE TO authenticated
        USING (auth.uid() = bruker_id);
        """
    supabase.rpc("execute_sql", {"sql": sql})

# 📋 Vis policyer
policyer = hent_policyer(valgt_tabell)
st.subheader(f"📋 Policyer for `{valgt_tabell}`")

if not policyer:
    st.warning("Ingen policyer funnet.")
else:
    for p in policyer:
        st.markdown(f"**{p['policyname']}** – `{p['cmd']}` for `{p['roles']}`")
        st.code(f"USING: {p['qual']}\nWITH CHECK: {p['check']}")
        if st.button(f"🗑️ Slett '{p['policyname']}'", key=p['policyname']):
            slett_policy(valgt_tabell, p['policyname'])
            st.rerun()

# ➕ Opprett anbefalte policyer
st.divider()
if st.button(f"➕ Opprett anbefalte policyer for `{valgt_tabell}`"):
    opprett_standard_policy(valgt_tabell)
    st.success("✅ Policyer opprettet.")
    st.rerun()
