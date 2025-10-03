import streamlit as st
from måltidslogikk import generer_dagsplan, fordel_kalorier
from supabase_klient import (
    test_tilkobling,
    registrer_vekt_db,
    hent_vektlogg_db
)
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Slankeapp", page_icon="🍽️")

# Supabase-status
if test_tilkobling():
    st.success("✅ Supabase-tilkobling aktiv")
else:
    st.error("❌ Klarte ikke å koble til Supabase – sjekk Secrets eller tabellstruktur")

# Banner og intro
st.image("https://www.infera.no/wp-content/uploads/2025/10/slankeapp.png", use_container_width=True)
st.caption("Enkel kaloriguide som hjelper deg å gå ned i vekt, følge målet og holde budsjett.")
st.title("Slankeapp 🍽️")
st.subheader("Din enkle kaloriguide")

# Brukerdata
st.write("### Personlig informasjon 🧍")
kjønn = st.radio("Kjønn", ["Mann", "Kvinne"])
alder = st.number_input("Alder", min_value=10, max_value=100, step=1)
høyde = st.number_input("Høyde (cm)", min_value=120.0, max_value=220.0, step=0.5)

# Vektmål
st.write("### Vektmål 🎯")
startvekt = st.number_input("Startvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, format="%.1f")
målvekt = st.number_input("Målvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, format="%.1f")

# Beregn BMR og TDEE
def beregn_bmr(vekt, høyde, alder, kjønn):
    if kjønn == "Mann":
        return 10 * vekt + 6.25 * høyde - 5 * alder + 5
    else:
        return 10 * vekt + 6.25 * høyde - 5 * alder - 161

if startvekt and høyde and alder:
    bmr = beregn_bmr(startvekt, høyde, alder, kjønn)
    tdee = bmr * 1.4  # Moderat aktiv
    anbefalt_kalorimål = int(tdee - 500)
    st.write(f"🧮 Beregnet BMR: {int(bmr)} kcal/dag")
    st.write(f"⚙️ Estimert TDEE: {int(tdee)} kcal/dag")
    st.write(f"🎯 Anbefalt kaloriinntak for vektnedgang: {anbefalt_kalorimål} kcal/dag")
else:
    anbefalt_kalorimål = 1800

# Kaloriinntak
kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, anbefalt_kalorimål)

# Kalorifordeling
fordeling = fordel_kalorier(kalorimål)
st.write("### Kalorifordeling per måltid")
for kategori, kcal in fordeling.items():
    st.write(f"{kategori}: {kcal} kcal")

# Måltidsplan
plan, total = generer_dagsplan(kalorimål)
st.write("### Dagens måltidsforslag")
for måltid in plan:
    st.markdown(f"**{måltid['kategori']} – {måltid['navn']}**")
    st.write(f"{måltid['kalorier']} kcal – ca. kr {måltid['pris']}")
    st.write(måltid["oppskrift"])
    st.divider()
st.write(f"**Totalt kalorier i dag:** {total} kcal")

# Vektlogg
st.write("### Vektlogg 📉")
dagens_vekt = st.number_input("Registrer dagens vekt (kg)", min_value=40.0, max_value=200.0, step=0.1)
bruker_id = "demo"  # Kan utvides med innlogging senere

if st.button("Lagre vekt"):
    registrer_vekt_db(bruker_id, str(date.today()), dagens_vekt)
    st.success(f"Vekt {dagens_vekt} kg lagret for {date.today()}")

data = hent_vektlogg_db(bruker_id)
df = pd.DataFrame(data)

if not df.empty:
    df["dato"] = pd.to_datetime(df["dato"])
    df = df.rename(columns={"dato": "Dato", "vekt": "Vekt"})
    st.line_chart(df.set_index("Dato")["Vekt"])
    st.write(df.tail())

    if startvekt > målvekt:
        siste_vekt = df["Vekt"].iloc[-1]
        fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1)
        st.write(f"**Siste registrerte vekt:** {siste_vekt} kg")
        st.write(f"**Målvekt:** {målvekt} kg")
        st.progress(fremdrift / 100)
        st.write(f"**Fremdrift mot mål:** {fremdrift}%")
    else:
        st.warning("Startvekten må være høyere enn målvekten for å vise fremdrift og prognose.")
else:
    st.info("Ingen vektdata registrert ennå.")
