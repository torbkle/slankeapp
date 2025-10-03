import streamlit as st
from supabase import create_client, Client

# 🔐 Hent Supabase-verdier fra Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# 🔌 Opprett klient
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Test tilkobling
def test_tilkobling():
    try:
        supabase.table("vektlogg").select("*").limit(1).execute()
        return True
    except Exception as e:
        print("Supabase-feil:", e)
        return False

# 📦 Lagre vekt
def registrer_vekt_db(bruker_id, dato, vekt):
    try:
        data = {"bruker_id": bruker_id, "dato": dato, "vekt": vekt}
        supabase.table("vektlogg").insert(data).execute()
    except Exception as e:
        print("Feil ved lagring av vekt:", e)

# 📤 Hent vektlogg
def hent_vektlogg_db(bruker_id):
    try:
        response = supabase.table("vektlogg").select("*").eq("bruker_id", bruker_id).order("dato").execute()
        return response.data
    except Exception as e:
        print("Feil ved henting av vektlogg:", e)
        return []

# 👥 Hent unike brukere
def hent_unike_brukere():
    try:
        response = supabase.table("vektlogg").select("bruker_id").execute()
        alle = [rad["bruker_id"] for rad in response.data if "bruker_id" in rad]
        return sorted(list(set(alle)))
    except Exception as e:
        print("Feil ved henting av brukere:", e)
        return []

# 🧍 Lagre personlig info
def lagre_brukerinfo(data):
    try:
        supabase.table("brukerinfo").upsert(data).execute()
    except Exception as e:
        print("Feil ved lagring av brukerinfo:", e)

# 🔍 Hent personlig info
def hent_brukerinfo(bruker_id):
    try:
        response = supabase.table("brukerinfo").select("*").eq("bruker_id", bruker_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print("Feil ved henting av brukerinfo:", e)
        return None
