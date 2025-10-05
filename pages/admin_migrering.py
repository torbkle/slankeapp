import streamlit as st
from supabase_klient import supabase

st.set_page_config(page_title="Admin Migrering", layout="centered")
st.title("🛠️ Admin – Migrering av bruker-ID")

def finn_ugyldige_rader(tabellnavn):
    response = supabase.table(tabellnavn)\
        .select("id, bruker_id")\
        .execute()
    return [rad for rad in response.data if "@" in rad["bruker_id"]]

def migrer_rader(tabellnavn):
    ugyldige = finn_ugyldige_rader(tabellnavn)
    oppdatert = 0
    for rad in ugyldige:
        epost = rad["bruker_id"]
        bruker = supabase.table("brukere").select("id").eq("email", epost).execute().data
        if bruker:
            ny_uuid = bruker[0]["id"]
            supabase.table(tabellnavn).update({"bruker_id": ny_uuid}).eq("id", rad["id"]).execute()
            oppdatert += 1
    return oppdatert

st.subheader("📏 Vektlogg")
ugyldige_vekt = finn_ugyldige_rader("vektlogg")
st.write(f"Ugyldige rader: {len(ugyldige_vekt)}")
if st.button("Migrer vektlogg"):
    antall = migrer_rader("vektlogg")
    st.success(f"✅ Oppdatert {antall} rader i vektlogg")

st.subheader("🍽️ Måltider")
ugyldige_maltid = finn_ugyldige_rader("måltider")
st.write(f"Ugyldige rader: {len(ugyldige_maltid)}")
if st.button("Migrer måltider"):
    antall = migrer_rader("måltider")
    st.success(f"✅ Oppdatert {antall} rader i måltider")
