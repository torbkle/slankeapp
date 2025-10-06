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
df["ny"] = df["opprettet"] == df["opprettet"].max()

st.subheader("🧑‍💻 Registrerte brukere")
styled_df = df[["email", "fornavn", "etternavn", "alder", "rolle", "opprettet", "ny"]].style.apply(
    lambda x: ["background-color: #dff0d8" if x.ny else "" for _ in x], axis=1
)
st.dataframe(styled_df, use_container_width=True)

# 📥 CSV-eksport
csv = df.drop(columns=["ny"]).to_csv(index=False).encode("utf-8")
st.download_button("📥 Last ned som CSV", data=csv, file_name="registreringslogg.csv", mime="text/csv")

# 🔁 Lenke tilbake til Auth Repair
st.markdown("🔁 [Gå tilbake til Auth Repair](./auth_repair)")
