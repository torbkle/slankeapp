import streamlit as st
from supabase_admin import supabase
import pandas as pd

st.set_page_config(page_title="Registreringslogg", layout="wide")
st.title("📋 Registreringslogg – Slankeapp")

# 🔍 Hent alle brukere fra tabellen
response = supabase.table("brukere").select("*").order("opprettet", desc=True).execute()

if response.status_code != 200:
    st.error("🚫 Klarte ikke hente brukere.")
    st.code(response.json())
    st.stop()

data = response.data

if not data:
    st.info("Ingen brukere er registrert ennå.")
    st.stop()

# 📊 Vis som tabell
df = pd.DataFrame(data)
df["opprettet"] = pd.to_datetime(df["opprettet"]).dt.strftime("%Y-%m-%d %H:%M")

st.subheader("🧑‍💻 Registrerte brukere")
st.dataframe(df[["email", "fornavn", "etternavn", "alder", "rolle", "opprettet"]], use_container_width=True)

# 📥 CSV-eksport
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Last ned som CSV", data=csv, file_name="registreringslogg.csv", mime="text/csv")
