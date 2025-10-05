import streamlit as st
import pandas as pd
from supabase_klient import supabase
from branding import vis_logo, vis_footer
from auth import krever_innlogging, er_admin

krever_innlogging()
st.set_page_config(page_title="Adminpanel", layout="wide")
vis_logo()
st.title("🛠️ Adminpanel – Slankeapp")

if not er_admin():
    st.warning("Du har ikke tilgang til adminpanelet.")
    st.stop()

# Brukeroversikt med søk og eksport
st.subheader("👥 Registrerte brukere")

try:
    brukere = supabase.table("brukere").select("*").execute().data
    df = pd.DataFrame(brukere)

    søk = st.text_input("🔍 Søk etter navn eller e-post")
    if søk:
        df = df[df["fornavn"].str.contains(søk, case=False) | df["etternavn"].str.contains(søk, case=False) | df["email"].str.contains(søk, case=False)]

    alder_filter = st.slider("Filtrer på alder", 10, 100, (10, 100))
    df = df[(df["alder"] >= alder_filter[0]) & (df["alder"] <= alder_filter[1])]

    st.dataframe(df[["fornavn", "etternavn", "alder", "email", "rolle"]], use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Last ned som CSV", data=csv, file_name="brukere.csv", mime="text/csv")
except Exception as e:
    st.error(f"Feil ved henting av brukere: {e}")

# Vektlogg
st.subheader("📊 Vektregistreringer")
try:
    vektdata = supabase.table("vektlogg").select("*").order("dato", desc=True).limit(50).execute().data
    df_vekt = pd.DataFrame(vektdata)
    st.dataframe(df_vekt, use_container_width=True)
except Exception as e:
    st.error(f"Feil ved henting av vektdata: {e}")

# Måltider
st.subheader("🍽️ Registrerte måltider")
try:
    maltider = supabase.table("måltider").select("*").order("tidspunkt", desc=True).limit(50).execute().data
    df_mat = pd.DataFrame(maltider)
    st.dataframe(df_mat, use_container_width=True)
except Exception as e:
    st.error(f"Feil ved henting av måltider: {e}")

vis_footer()
