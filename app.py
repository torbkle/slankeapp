import streamlit as st

st.set_page_config(page_title="Slankepp", page_icon="🍽️")

st.title("Slankepp 🍽️")
st.subheader("Din enkle kaloriguide")

# Brukerinput
kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, 1800)

# Eksempel på måltidsforslag
from måltidslogikk import generer_dagsplan

plan = generer_dagsplan(kalorimål)
for måltid in plan:
    st.markdown(f"**{måltid['navn']}** – {måltid['kalorier']} kcal")
    st.write(måltid["oppskrift"])


st.write("### Dagens måltidsforslag")
for måltid in måltider:
    st.markdown(f"**{måltid['navn']}** – {måltid['kalorier']} kcal")
    st.write(måltid["oppskrift"])
