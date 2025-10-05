import streamlit as st
from datetime import date
from branding import vis_logo, vis_footer
from auth import login_form, signup_form, logg_ut_knapp, krever_innlogging, er_admin
from maltidslogikk import vis_maltider, registrer_maltid
from oppskrift_api import hent_oppskrifter
from supabase_klient import supabase

# Konfigurasjon
st.set_page_config(page_title="Slankeapp", layout="centered")
vis_logo()
st.title("🥗 Slankeapp – Din daglige helseassistent")

# Autentisering
def auth_panel():
    if "innlogget" not in st.session_state or not st.session_state["innlogget"]:
        st.sidebar.markdown("## 🔐 Autentisering")
        valg = st.sidebar.radio("Velg handling", ["Logg inn", "Registrer ny bruker"])
        if valg == "Logg inn":
            login_form()
        else:
            signup_form()
    else:
        st.sidebar.markdown(f"👋 Logget inn som **{st.session_state['navn']}**")
        logg_ut_knapp()

auth_panel()
krever_innlogging()

# Bruker-ID fra session
bruker_id = st.session_state.get("bruker_id")

# Vektregistrering
def registrer_vekt(vekt):
    try:
        eksisterende = supabase.table("vektlogg")\
            .select("id")\
            .eq("bruker_id", bruker_id)\
            .eq("dato", str(date.today()))\
            .execute()
        if eksisterende.data:
            supabase.table("vektlogg").update({"vekt": vekt})\
                .eq("id", eksisterende.data[0]["id"]).execute()
        else:
            supabase.table("vektlogg").insert({
                "bruker_id": bruker_id,
                "dato": str(date.today()),
                "vekt": vekt
            }).execute()
        return True
    except Exception as e:
        st.error(f"Feil ved lagring: {e}")
        return False

def hent_siste_vekt():
    try:
        response = supabase.table("vektlogg")\
            .select("vekt, dato")\
            .eq("bruker_id", bruker_id)\
            .order("dato", desc=True)\
            .limit(1)\
            .execute()
        if response.data:
            return response.data[0]["vekt"], response.data[0]["dato"]
        else:
            return None, None
    except Exception as e:
        st.error(f"Feil ved henting av vekt: {e}")
        return None, None

# Seksjon: Registrer vekt
st.subheader("📏 Registrer dagens vekt")
siste_vekt, siste_dato = hent_siste_vekt()
if siste_vekt:
    st.markdown(f"📅 Sist registrert: **{siste_dato}** – **{siste_vekt} kg**")

ny_vekt = st.number_input("Din vekt i dag (kg)", min_value=30.0, max_value=250.0, step=0.1)
if st.button("Lagre vekt"):
    if registrer_vekt(ny_vekt):
        st.success("✅ Vekt registrert!")

# Seksjon: Måltider
st.subheader("🍽️ Registrer måltid")
registrer_maltid(bruker_id)

st.subheader("📋 Dine måltider")
vis_maltider(bruker_id)

vis_footer()
