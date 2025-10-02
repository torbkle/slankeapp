import streamlit as st
from måltidslogikk import generer_dagsplan
from vektlogg import registrer_vekt, hent_vektlogg, beregn_fremdrift
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Slankepp", page_icon="🍽️")

st.title("Slankepp 🍽️")
st.subheader("Din enkle kaloriguide")

# Brukerinput for kaloriinntak
kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, 1800)

# Generer måltidsplan
plan, total = generer_dagsplan(kalorimål)

st.write("### Dagens måltidsforslag")
for måltid in plan:
    st.markdown(f"**{måltid['kategori']} – {måltid['navn']}**")
    st.write(f"{måltid['kalorier']} kcal – ca. kr {måltid['pris']}")
    st.write(måltid["oppskrift"])
    st.divider()

st.write(f"**Totalt kalorier i dag:** {total} kcal")

# Vektloggseksjon
st.write("### Vektlogg 📉")

dagens_vekt = st.number_input("Registrer dagens vekt (kg)", min_value=40.0, max_value=200.0, step=0.1)
if st.button("Lagre vekt"):
    registrer_vekt(str(date.today()), dagens_vekt)
    st.success(f"Vekt {dagens_vekt} kg lagret for {date.today()}")

df = hent_vektlogg()
if not df.empty:
    st.line_chart(df.set_index("Dato")["Vekt"])
    st.write(df.tail())

    # Fremdrift mot mål
    startvekt = 83.0
    målvekt = 76.0
    fremdrift, siste_vekt = beregn_fremdrift(startvekt, målvekt, df)

    st.write(f"**Siste registrerte vekt:** {siste_vekt} kg")
    st.write(f"**Målvekt:** {målvekt} kg")
    st.progress(fremdrift / 100)
    st.write(f"**Fremdrift mot mål:** {fremdrift}%")
else:
    st.info("Ingen vektdata registrert ennå.")
