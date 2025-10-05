import streamlit as st
import pandas as pd
from supabase_klient import supabase

st.set_page_config(page_title="Brukeroversikt", layout="wide")
st.title("👥 Brukeroversikt – Slankeapp")

# 1. Hent alle brukere
def hent_brukere():
    response = supabase.table("brukere").select("*").execute()
    return response.data if response.data else []

brukere = hent_brukere()
df = pd.DataFrame(brukere)

if df.empty:
    st.warning("Ingen brukere registrert ennå.")
    st.stop()

# 2. Vis tabell
st.subheader("📋 Registrerte brukere")
st.dataframe(df[["id", "email", "rolle", "alder"]], use_container_width=True)

# 3. Velg bruker for handling
st.subheader("⚙️ Administrer bruker")
valgt_email = st.selectbox("Velg e-post", df["email"])

valgt = df[df["email"] == valgt_email].iloc[0]
st.write(f"**ID:** `{valgt['id']}`")
st.write(f"**Rolle:** `{valgt['rolle']}`")
st.write(f"**Alder:** `{valgt['alder']}`")

# 4. Rediger rolle
ny_rolle = st.text_input("Ny rolle", value=valgt["rolle"])
if st.button("🔄 Oppdater rolle"):
    supabase.table("brukere").update({"rolle": ny_rolle}).eq("id", valgt["id"]).execute()
    st.success("✅ Rolle oppdatert!")

# 5. Slett bruker
if st.button("🗑️ Slett bruker"):
    supabase.table("brukere").delete().eq("id", valgt["id"]).execute()
    st.warning(f"🚫 Bruker med e-post `{valgt_email}` er slettet.")

# 6. (Valgfritt) Eksporter til CSV
with st.expander("📤 Eksporter til CSV"):
    st.download_button("Last ned CSV", df.to_csv(index=False), file_name="brukere.csv")
