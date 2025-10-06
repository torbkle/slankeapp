from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
public_key = os.getenv("SUPABASE_PUBLIC_KEY")

supabase = create_client(url, public_key)

