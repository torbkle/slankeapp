import streamlit as st

st.set_page_config(page_title="Slankepp", page_icon="🍽️")

st.title("Slankepp 🍽️")
st.subheader("Din enkle kaloriguide")

# Brukerinput
kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, 1800)

# Eksempel på måltidsforslag
måltider = [
    {"navn": "Havregrøt med eple", "kalorier": 300, "oppskrift": "Kok havregryn med vann, topp med eplebiter."},
    {"navn": "Kyllingsalat", "kalorier": 450, "oppskrift": "Grillet kylling, salat, couscous, dressing."},
    {"navn": "Torsk med grønnsaker", "kalorier": 550, "oppskrift": "Ovnsbakt torsk med brokkoli og gulrot."},
    {"navn": "Cottage cheese med bær", "kalorier": 350, "oppskrift": "Bland cottage cheese med frosne bær."}
]

st.write("### Dagens måltidsforslag")
for måltid in måltider:
    st.markdown(f"**{måltid['navn']}** – {måltid['kalorier']} kcal")
    st.write(måltid["oppskrift"])
