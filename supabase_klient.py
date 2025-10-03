from supabase import create_client
from dotenv import load_dotenv
import os

# Last inn miljøvariabler fra .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def registrer_vekt_db(bruker_id, dato, vekt):
    data = {"bruker_id": bruker_id, "dato": dato, "vekt": vekt}
    supabase.table("vektlogg").insert(data).execute()

def hent_vektlogg_db(bruker_id):
    response = supabase.table("vektlogg").select("*").eq("bruker_id", bruker_id).order("dato").execute()
    return response.data
