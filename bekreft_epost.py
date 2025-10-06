import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def bekreft_epost(uid: str):
    if not SUPABASE_URL or not SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_URL eller SERVICE_ROLE_KEY mangler i miljøvariabler.")

    url = f"{SUPABASE_URL}/auth/v1/admin/users/{uid}"
    headers = {
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email_confirmed": True
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"✅ E-post bekreftet for UID: {uid}")
        else:
            print(f"⚠️ Feil ved bekreftelse – status {response.status_code}")
            print(response.text)
        return response
    except Exception as e:
        print("🚫 Feil under API-kall til Supabase Admin.")
        print(str(e))
        raise
