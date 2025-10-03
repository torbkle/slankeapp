import os
import random
import requests

# 🔐 API-konfigurasjon
API_URL = "https://api.mrcook.app/recipes/generate"
API_KEY = os.getenv("OPPSKRIFT_API_KEY")  # legg inn i .env eller Streamlit secrets

def generer_oppskrift(kategori, kalorimål):
    if API_KEY:
        try:
            response = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"category": kategori, "calories": kalorimål}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "navn": data["name"],
                    "kalorier": data["calories"],
                    "bilde_url": data["image_url"],
                    "oppskrift": data["instructions"],
                    "pris": round(data["calories"] * 0.02, 1)
                }
        except Exception as e:
            print(f"API-feil: {e}")

    # 🔁 Fallback til mock hvis API feiler eller mangler
    return random.choice(mock_oppskrifter(kategori, kalorimål))

def mock_oppskrifter(kategori, kalorimål):
    return {
        "Frokost": [
            {
                "navn": "Havregrøt med bær",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
                "oppskrift": "Kok havregryn med melk, topp med blåbær og honning.",
                "pris": round(kalorimål * 0.02, 1)
            }
        ],
        "Lunsj": [
            {
                "navn": "Kyllingsalat",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1562967916-eb82221dfb36",
                "oppskrift": "Grillet kylling med salat, avokado og vinaigrette.",
                "pris": round(kalorimål * 0.025, 1)
            }
        ],
        "Middag": [
            {
                "navn": "Laks med grønnsaker",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1604908177522-4021d3a1e7d3",
                "oppskrift": "Ovnsbakt laks med brokkoli og søtpotet.",
                "pris": round(kalorimål * 0.03, 1)
            }
        ],
        "Kveldsmat": [
            {
                "navn": "Tunfiskwrap",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1613145993481-1b6b2b3b3b3b",
                "oppskrift": "Fullkornswrap med tunfisk, salat og lett dressing.",
                "pris": round(kalorimål * 0.019, 1)
            }
        ]
    }.get(kategori, [])
