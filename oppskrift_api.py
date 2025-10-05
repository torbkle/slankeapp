import os
import random
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPPSKRIFT_API_KEY")
API_URL = "https://api.mrcook.app/recipes/generate"

def generer_oppskrift(kategori, kalorimål):
    if API_KEY:
        try:
            response = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "category": kategori,
                    "calories": kalorimål,
                    "language": "no",
                    "format": "json"
                }
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "navn": data.get("name", "Ukjent måltid"),
                    "kalorier": data.get("calories", kalorimål),
                    "bilde_url": data.get("image_url", ""),
                    "oppskrift": data.get("instructions", "Ingen instruksjoner tilgjengelig."),
                    "pris": round(data.get("calories", kalorimål) * 0.02, 1)
                }
        except Exception as e:
            print(f"API-feil: {e}")
    # Fallback til mock
    return random.choice(mock_oppskrifter(kategori, kalorimål))

def mock_oppskrifter(kategori, kalorimål):
    return {
        "Frokost": [{
            "navn": "Havregrøt med bær",
            "kalorier": kalorimål,
            "bilde_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
            "oppskrift": "Kok havregryn med melk, topp med blåbær og honning.",
            "pris": round(kalorimål * 0.02, 1)
        }],
        "Lunsj": [{
            "navn": "Kyllingsalat",
            "kalorier": kalorimål,
            "bilde_url": "https://images.unsplash.com/photo-1562967916-eb82221dfb36",
            "oppskrift": "Grillet kylling med salat, avokado og vinaigrette.",
            "pris": round(kalorimål * 0.025, 1)
        }],
        "Middag": [{
            "navn": "Laks med grønnsaker",
            "kalorier": kalorimål,
            "bilde_url": "https://images.unsplash.com/photo-1604908177522-4021d3a1e7d3",
            "oppskrift": "Ovnsbakt laks med brokkoli og søtpotet.",
            "pris": round(kalorimål * 0.03, 1)
        }],
        "Kveldsmat": [{
            "navn": "Tunfiskwrap",
            "kalorier": kalorimål,
            "bilde_url": "https://images.unsplash.com/photo-1613145993481-1b6b2b3b3b3b",
            "oppskrift": "Fullkornswrap med tunfisk, salat og lett dressing.",
            "pris": round(kalorimål * 0.019, 1)
        }]
    }.get(kategori, [])

def hent_oppskrifter():
    st.write("🔍 Foreslåtte oppskrifter basert på måltidstype:")
    for kategori in ["Frokost", "Lunsj", "Middag", "Kveldsmat"]:
        oppskrift = generer_oppskrift(kategori, random.randint(300, 600))
        st.markdown(f"### {kategori}: {oppskrift['navn']}")
        if oppskrift["bilde_url"]:
            st.image(oppskrift["bilde_url"], width=300)
        st.write(f"**Kalorier:** {oppskrift['kalorier']} kcal")
        st.write(f"**Pris (estimert):** {oppskrift['pris']} kr")
        st.write(f"**Oppskrift:** {oppskrift['oppskrift']}")
        st.markdown("---")
