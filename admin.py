import streamlit as st
from supabase_klient import supabase
from branding import vis_logo, vis_footer
from auth import krever_innlogging

krever_innlogging()
st.set_page_config(page_title="Adminpanel", layout="wide")
vis_logo()
st.title("🛠️ Adminpanel – Slankeapp")

# Sjekk om bruker er admin
admin_email = "torbjorn@infera.no"
if st.session_state.get("innlogget") and st.session_state.get("bruker_id"):
    if st.session_state.get("navn") != "Torbjørn":
        st.warning("Du har ikke tilgang til adminpanelet.")
        st.stop()

# Brukeroversikt
st.subheader("👥 Registrerte brukere")
try:
    brukere = supabase.table("brukere").select("fornavn, etternavn, alder, email").execute().data
    for b in brukere:
        st.markdown(f"- **{b['fornavn']} {b['etternavn']}** ({b['alder']} år) – {b['email']}")
except Exception as e:
    st.error(f"Feil ved henting av brukere: {e}")

# Vektlogg
st.subheader("📊 Vektregistreringer")
try:
    vektdata = supabase.table("vektlogg").select("*").order("dato", desc=True).limit(20).execute().data
    for v in vektdata:
        st.write(f"{v['bruker_id']} – {v['dato']}: {v['vekt']} kg")
except Exception as e:
    st.error(f"Feil ved henting av vektdata: {e}")

# Måltider
st.subheader("🍽️ Registrerte måltider")
try:
    maltider = supabase.table("måltider").select("*").order("tidspunkt", desc=True).limit(20).execute().data
    for m in maltider:
        st.write(f"{m['bruker_id']} – {m['tidspunkt']}: {m['kategori']} ({m['kalorier']} kcal)")
except Exception as e:
    st.error(f"Feil ved henting av måltider: {e}")

vis_footer()
