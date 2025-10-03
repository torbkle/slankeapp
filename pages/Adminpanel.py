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
st.write(f"Totalt antall brukere: **{len(brukere)}**")

# 📊 Aggregert statistikk
total_nedgang = 0
aktive_brukere = 0
fremdrift_liste = []

for bruker_id in brukere:
    info = hent_brukerinfo(bruker_id)
    if not info:
        continue

    startvekt = info.get("startvekt")
    målvekt = info.get("målvekt")
    logg = hent_vektlogg_db(bruker_id)

    if logg and startvekt and målvekt and startvekt > målvekt:
        siste_vekt = logg[-1]["vekt"]
        nedgang = startvekt - siste_vekt
        fremdrift = round(nedgang / (startvekt - målvekt) * 100, 1)
        total_nedgang += nedgang
        aktive_brukere += 1
        fremdrift_liste.append((bruker_id, fremdrift, siste_vekt))

# 📈 Vis aggregert data
if aktive_brukere > 0:
    gjennomsnitt_nedgang = round(total_nedgang / aktive_brukere, 2)
    st.write(f"📉 Gjennomsnittlig vektnedgang: **{gjennomsnitt_nedgang} kg**")
    st.write(f"📈 Aktive brukere med fremdrift: **{aktive_brukere}**")

    st.write("### Fremdrift per bruker")
    for bruker_id, fremdrift, siste_vekt in fremdrift_liste:
        st.write(f"**{bruker_id}** – Siste vekt: {siste_vekt} kg – Fremdrift: {fremdrift}%")
        st.progress(fremdrift / 100)
else:
    st.info("Ingen brukere med registrert fremdrift ennå.")

# 🔍 Detaljvisning
st.write("---")
valgt = st.selectbox("Velg bruker for detaljvisning", brukere)
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
