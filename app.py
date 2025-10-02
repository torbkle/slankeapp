import streamlit as st
from måltidslogikk import generer_dagsplan, fordel_kalorier
from vektlogg import (
    registrer_vekt,
    hent_vektlogg,
    beregn_fremdrift,
    estimer_tid_til_mål
)
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Slankepp", page_icon="🍽️")

# Banner og intro
st.image("https://www.infera.no/wp-content/uploads/2025/10/slankeapp.png", use_container_width=True)
st.caption("Enkel kaloriguide som hjelper deg å gå ned i vekt, følge målet og holde budsjett.")
st.title("Slankepp 🍽️")
st.subheader("Din enkle kaloriguide")

# Vektmål uten forhåndsverdi
st.write("### Vektmål 🎯")
startvekt = st.number_input("Startvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, format="%.1f")
målvekt = st.number_input("Målvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, format="%.1f")

# Kaloriinntak
kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, 1800)

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
if st.button("Lagre vekt"):
    registrer_vekt(str(date.today()), dagens_vekt)
    st.success(f"Vekt {dagens_vekt} kg lagret for {date.today()}")

df = hent_vektlogg()
if not df.empty:
    st.line_chart(df.set_index("Dato")["Vekt"])
    st.write(df.tail())

    # Sjekk at startvekt og målvekt er gyldige
    if startvekt > målvekt:
        fremdrift, siste_vekt = beregn_fremdrift(startvekt, målvekt, df)
        st.write(f"**Siste registrerte vekt:** {siste_vekt} kg")
        st.write(f"**Målvekt:** {målvekt} kg")
        st.progress(fremdrift / 100)
        st.write(f"**Fremdrift mot mål:** {fremdrift}%")

        est_dager, måldato = estimer_tid_til_mål(startvekt, målvekt, df)
        if måldato:
            st.write(f"📅 Estimert tid til målvekt: {est_dager} dager")
            st.write(f"🎯 Prognose: Du når {målvekt} kg rundt {måldato.strftime('%d.%m.%Y')}")
        else:
            st.info("For lite data til å beregne prognose.")
    else:
        st.warning("Startvekten må være høyere enn målvekten for å vise fremdrift og prognose.")
else:
    st.info("Ingen vektdata registrert ennå.")
