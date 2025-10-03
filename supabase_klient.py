import streamlit as st
from supabase import create_client

# Hent Supabase-verdier fra Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Opprett klient
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Lagre vekt
def registrer_vekt_db(bruker_id, dato, vekt):
    data = {"bruker_id": bruker_id, "dato": dato, "vekt": vekt}
    supabase.table("vektlogg").insert(data).execute()

# Hent vektlogg
def hent_vektlogg_db(bruker_id):
    response = supabase.table("vektlogg").select("*").eq("bruker_id", bruker_id).order("dato").execute()
    return response.data

# Test tilkobling
def test_tilkobling():
    try:
        supabase.table("vektlogg").select("*").limit(1).execute()
        return True
    except Exception as e:
        print("Supabase-feil:", e)
        return False
