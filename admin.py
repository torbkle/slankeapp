import streamlit as st
import pandas as pd
from supabase_klient import hent_unike_brukere, hent_vektlogg_db, hent_brukerinfo

st.set_page_config(page_title="Adminpanel · Slankeapp", page_icon="🛠️")

st.title("🛠️ Adminpanel")
st.caption("Kun for autoriserte brukere.")

# 🔐 Enkel tilgangskontroll
passord = st.text_input("Adminpassord", type="password")
if passord != st.secrets.get("ADMIN_PASSORD", ""):
    st.error("⛔ Feil passord eller mangler tilgang.")
    st.stop()

# ✅ Oversikt
brukere = hent_unike_brukere()
admin_data = []

for bruker in brukere:
    logg = hent_vektlogg_db(bruker)
    info = hent_brukerinfo(bruker)
    if logg and info:
        df = pd.DataFrame(logg)
        if len(df) > 0:
            siste_vekt = df["vekt"].iloc[-1]
            startvekt = float(info.get("startvekt", 0))
            målvekt = float(info.get("målvekt", 0))
            fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1) if startvekt > målvekt else 0
            admin_data.append({
                "Bruker": bruker,
                "Kjønn": info.get("kjønn", ""),
                "Alder": info.get("alder", ""),
                "Startvekt": startvekt,
                "Målvekt": målvekt,
                "Siste vekt": siste_vekt,
                "Fremdrift (%)": fremdrift
            })

if admin_data:
    st.dataframe(pd.DataFrame(admin_data))
else:
    st.info("Ingen brukere med fullstendig data.")
