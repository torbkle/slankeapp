import streamlit as st
from supabase import create_client, Client

# 🔐 Hent hemmeligheter fra Streamlit Cloud
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 🔌 Opprett klient
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Test tilkobling
def test_tilkobling():
    try:
        response = supabase.table("brukerinfo").select("*").limit(1).execute()
        return True
    except Exception as e:
        print("Supabase-feil:", e)
        return False

# 📥 Hent alle brukere
def hent_unike_brukere():
    try:
        data = supabase.table("brukerinfo").select("bruker_id").execute()
        return [row["bruker_id"] for row in data.data]
    except Exception as e:
        print("Feil ved henting av brukere:", e)
        return []

# 📤 Lagre brukerinfo
def lagre_brukerinfo(info):
    try:
        supabase.table("brukerinfo").upsert(info).execute()
    except Exception as e:
        print("Feil ved lagring av brukerinfo:", e)

# 📥 Hent brukerinfo
def hent_brukerinfo(bruker_id):
    try:
        data = supabase.table("brukerinfo").select("*").eq("bruker_id", bruker_id).single().execute()
        return data.data
    except Exception as e:
        print("Feil ved henting av brukerinfo:", e)
        return {}

# 📤 Registrer vekt
def registrer_vekt_db(bruker_id, dato, vekt):
    try:
        supabase.table("vektlogg").insert({
            "bruker_id": bruker_id,
            "dato": dato,
            "vekt": vekt
        }).execute()
    except Exception as e:
        print("Feil ved lagring av vekt:", e)

# 📥 Hent vektlogg
def hent_vektlogg_db(bruker_id):
    try:
        data = supabase.table("vektlogg").select("*").eq("bruker_id", bruker_id).order("dato").execute()
        return data.data
    except Exception as e:
        print("Feil ved henting av vektlogg:", e)
        return []
