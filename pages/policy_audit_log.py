import streamlit as st
from supabase_klient import supabase
import pandas as pd

st.set_page_config(page_title="Policy Audit Log", layout="wide")
st.title("📜 Policy Audit Log – RLS-historikk")

# 📋 Hent policyhistorikk (krever audit-tabell)
def hent_audit_logg():
    try:
        response = supabase.table("audit_policy_logg").select("*").order("tidspunkt", desc=True).execute()
        return pd.DataFrame(response.data)
    except Exception:
        st.warning("Ingen audit-tabell funnet. Du må aktivere audit logging.")
        return pd.DataFrame()

# 📋 Vis logg
df = hent_audit_logg()

if df.empty:
    st.info("Ingen policyendringer registrert ennå.")
    st.stop()

# 🔍 Filtrering
tabeller = df["tabell"].unique().tolist()
valgt_tabell = st.selectbox("Filtrer etter tabell", tabeller)
df = df[df["tabell"] == valgt_tabell]

policyer = df["policy_navn"].unique().tolist()
valgt_policy = st.selectbox("Filtrer etter policy", policyer)
df = df[df["policy_navn"] == valgt_policy]

# 📊 Vis tabell
st.subheader(f"Endringslogg for `{valgt_policy}` i `{valgt_tabell}`")
st.dataframe(df[["tidspunkt", "handling", "utført_av", "policy_sql"]], use_container_width=True)
