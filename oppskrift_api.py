import random

def generer_oppskrift(kategori, kalorimål):
    # 🔧 Dette er en mock – bytt ut med ekte API-kall senere
    forslag = {
        "Frokost": [
            {
                "navn": "Havregrøt med bær",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
                "oppskrift": "Kok havregryn med melk, topp med blåbær og honning."
            }
        ],
        "Lunsj": [
            {
                "navn": "Kyllingsalat",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1562967916-eb82221dfb36",
                "oppskrift": "Grillet kylling med salat, avokado og vinaigrette."
            }
        ],
        "Middag": [
            {
                "navn": "Laks med grønnsaker",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1604908177522-4021d3a1e7d3",
                "oppskrift": "Ovnsbakt laks med brokkoli og søtpotet."
            }
        ],
        "Kveldsmat": [
            {
                "navn": "Tunfiskwrap",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1605478371619-3b6b2b3b3b3b",
                "oppskrift": "Fullkornswrap med tunfisk, salat og lett dressing."
            }
        ]
    }
    return random.choice(forslag.get(kategori, []))
