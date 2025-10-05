import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Policy Manager", layout="wide")
st.title("🔐 Policy Manager – RLS-kontroll")

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

# ✅ Test om auth.uid() matcher id/bruker_id
def test_policy(tabell):
    try:
        user = supabase.auth.get_user().user
        uid = user.id
        st.success(f"Du er innlogget som `{uid}`")

        test_data = {
            "brukere": {"id": uid, "email": "test@policy.no", "fornavn": "Test", "etternavn": "Bruker", "alder": 99, "rolle": "debug"},
            "vektlogg": {"bruker_id": uid, "dato": "2025-10-05", "vekt": 88.8},
            "måltider": {"bruker_id": uid, "tidspunkt": "2025-10-05T12:00:00", "beskrivelse": "Testmåltid"}
        }

        response = supabase.table(tabell).insert(test_data[tabell]).execute()

        if response.status_code == 201:
            st.success("✅ RLS-policyen godtar innsetting.")
        else:
            st.error("🚫 RLS-policyen blokkerer innsetting.")
            st.code(response.json(), language="json")

    except Exception as e:
        st.error("🚫 Ikke innlogget eller feil ved test.")
        st.code(str(e), language="json")

# 📋 Vis policyer
policyer = hent_policyer(valgt_tabell)
st.subheader(f"📋 Policyer for `{valgt_tabell}`")

if not policyer:
    st.warning("Ingen policyer funnet.")
else:
    for p in policyer:
        status = "✅" if "auth.uid()" in (p["qual"] or "") + (p["check"] or "") else "⚠️"
        st.markdown(f"{status} **{p['policyname']}** – `{p['cmd']}` for `{p['roles']}`")
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

# 🚦 Test policy
st.divider()
if st.button(f"🚦 Test RLS-policy for `{valgt_tabell}`"):
    test_policy(valgt_tabell)
