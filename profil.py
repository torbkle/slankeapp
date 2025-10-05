import streamlit as st
from supabase_klient import supabase
from auth import krever_innlogging
from branding import vis_logo, vis_footer

krever_innlogging()
vis_logo()
st.title("👤 Din profil")

bruker_id = st.session_state["bruker_id"]

# Hent brukerdata
try:
    response = supabase.table("brukere").select("*").eq("id", bruker_id).execute()
    bruker = response.data[0]
except Exception as e:
    st.error(f"Feil ved henting av brukerdata: {e}")
    st.stop()

# Redigerbar form
with st.form("profilform"):
    fornavn = st.text_input("Fornavn", value=bruker["fornavn"])
    etternavn = st.text_input("Etternavn", value=bruker["etternavn"])
    alder = st.number_input("Alder", min_value=10, max_value=120, value=bruker["alder"])
    ny_passord = st.text_input("Nytt passord (valgfritt)", type="password")
    lagre = st.form_submit_button("💾 Oppdater profil")

    if lagre:
        oppdatering = {
            "fornavn": fornavn.strip(),
            "etternavn": etternavn.strip(),
            "alder": int(alder)
        }
        if ny_passord:
            oppdatering["passord"] = ny_passord
        try:
            supabase.table("brukere").update(oppdatering).eq("id", bruker_id).execute()
            st.success("✅ Profil oppdatert!")
        except Exception as e:
            st.error(f"Feil ved oppdatering: {e}")

vis_footer()
