import streamlit as st
from måltidslogikk import generer_dagsplan

st.set_page_config(page_title="Slankepp", page_icon="🍽️")

st.title("Slankepp 🍽️")
st.subheader("Din enkle kaloriguide")

# Brukerinput
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

