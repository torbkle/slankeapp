import streamlit as st
from datetime import date
from supabase_klient import supabase

# Importer moduler
from måltidslogikk import vis_måltider, registrer_måltid
from oppskrift_api import hent_oppskrifter
from branding import vis_logo, vis_footer

st.set_page_config(page_title="Slankeapp", layout="centered")

# Logo og tittel
vis_logo()
st.title("🥗 Slankeapp – Din daglige helseassistent")

# Midlertidig bruker-ID (erstatt med ekte innlogging senere)
bruker_id = "demo_bruker_123"

# Funksjon for å registrere dagens vekt
def registrer_vekt(bruker_id, vekt):
    try:
        eksisterende = supabase.table("vektlogg")\
            .select("id")\
            .eq("bruker_id", bruker_id)\
            .eq("dato", str(date.today()))\
            .execute()

        if eksisterende.data:
            supabase.table("vektlogg").update({
                "vekt": vekt
            }).eq("id", eksisterende.data[0]["id"]).execute()
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

# Funksjon for å hente siste registrerte vekt
def hent_siste_vekt(bruker_id):
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

# Seksjon: Registrer dagens vekt
st.subheader("📏 Registrer dagens vekt")
dagens_vekt = st.number_input("Din vekt i kg", min_value=30.0, max_value=200.0, step=0.1)

if st.button("Lagre vekt"):
    if registrer_vekt(bruker_id, dagens_vekt):
        st.success("✅ Vekt registrert!")

# Seksjon: Vis siste vekt
siste_vekt, siste_dato = hent_siste_vekt(bruker_id)
if siste_vekt:
    st.info(f"Siste registrerte vekt: **{siste_vekt} kg** ({siste_dato})")
else:
    st.warning("Ingen vekt registrert enda.")

# Seksjon: Måltider
st.subheader("🍽️ Dine måltider i dag")
vis_måltider(bruker_id)

st.subheader("➕ Registrer nytt måltid")
registrer_måltid(bruker_id)

# Seksjon: Oppskrifter
st.subheader("📸 Oppskriftsforslag")
hent_oppskrifter()

# Footer
vis_footer()
