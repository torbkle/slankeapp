# supabase_klient.py
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zewmjurylmyjweyqotpw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpld21qdXJ5bG15andleXFvdHB3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTQwMDA5NiwiZXhwIjoyMDc0OTc2MDk2fQ.8DfBdida1EE9RggZQnkARzvod2XR00isq8cXHXOWaQ8")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
