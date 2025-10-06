import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def bekreft_epost(uid):
    url = f"https://zewmjurylmyjweyqotpw.supabase.co/auth/v1/admin/users/{uid}"
    headers = {
        "apikey": os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        "Authorization": f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "email_confirmed_at": datetime.datetime.utcnow().isoformat()
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response
