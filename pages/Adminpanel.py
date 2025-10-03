import streamlit as st
import pandas as pd
from supabase_klient import hent_unike_brukere, hent_vektlogg_db, hent_brukerinfo, test_tilkobling

st.set_page_config(page_title="Adminpanel", page_icon="🔒")

st.title("🔒 Adminpanel")
st.caption("Kun for administratorer")

# 🔐 Passordbeskyttelse
passord = st.text_input("Adminpassord", type="password")
if passord != st.secrets.get("ADMIN_PASSORD", ""):
    st.warning("⛔ Feil passord eller mangler tilgang.")
    st.stop()

# ✅ Supabase-test
if not test_tilkobling():
    st.error("❌ Klarte ikke å koble til Supabase")
    st.stop()

# 👥 Brukeroversikt
st.write("## Brukere i systemet")
brukere = hent_unike_brukere()
valgt = st.selectbox("Velg bruker", brukere)

if valgt:
    info = hent_brukerinfo(valgt)
    st.write("### Profilinformasjon")
    st.json(info)

    st.write("### Vektlogg")
    data = hent_vektlogg_db(valgt)
    df = pd.DataFrame(data)

    if not df.empty:
        df["dato"] = pd.to_datetime(df["dato"])
        df = df.rename(columns={"dato": "Dato", "vekt": "Vekt"})
        st.line_chart(df.set_index("Dato")["Vekt"])
        st.write(df.tail())
    else:
        st.info("Ingen vektdata registrert for denne brukeren.")
