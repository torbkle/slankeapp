import streamlit as st
from datetime import date
from branding import vis_logo, vis_footer
from auth import login_form, registrer_ny_bruker, logg_ut_knapp, krever_innlogging
from maltidslogikk import vis_maltider, registrer_maltid
from oppskrift_api import hent_oppskrifter
from supabase_klient import supabase

# Autentisering
login_form()
registrer_ny_bruker()
logg_ut_knapp()
krever_innlogging()

# Konfigurasjon
st.set_page_config(page_title="Slankeapp", layout="centered")
vis_logo()
st.title("🥗 Slankeapp – Din daglige helseassistent")

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
            supabase.table("vektlogg").update({ "vekt": vekt })\
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
dagens_vekt = st.number_input("Din vekt i kg", min_value=30.0, max_value=200.0, step=0.1)
if st.button("Lagre vekt"):
    if registrer_vekt(dagens_vekt):
        st.success("✅ Vekt registrert!")

# Seksjon: Siste vekt
siste_vekt, siste_dato = hent_siste_vekt()
if siste_vekt:
    st.info(f"Siste registrerte vekt: **{siste_vekt} kg** ({siste_dato})")
else:
    st.warning("Ingen vekt registrert enda.")

# Seksjon: Måltider
st.subheader("🍽️ Dine måltider i dag")
vis_maltider(bruker_id)

st.subheader("➕ Registrer nytt måltid")
registrer_maltid(bruker_id)

# Seksjon: Oppskrifter
st.subheader("📸 Oppskriftsforslag")
hent_oppskrifter()

# Footer
vis_footer()
