import random

def generer_oppskrift(kategori, kalorimål):
    # 🔧 Mockbaserte forslag – bytt ut med ekte API senere
    forslag = {
        "Frokost": [
            {
                "navn": "Havregrøt med bær",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
                "oppskrift": "Kok havregryn med melk, topp med blåbær og honning.",
                "pris": round(kalorimål * 0.02, 1)
            },
            {
                "navn": "Smoothie med banan og spinat",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1590080877037-7c1c9b1c1c1c",
                "oppskrift": "Blend banan, spinat, yoghurt og havregryn.",
                "pris": round(kalorimål * 0.018, 1)
            }
        ],
        "Lunsj": [
            {
                "navn": "Kyllingsalat",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1562967916-eb82221dfb36",
                "oppskrift": "Grillet kylling med salat, avokado og vinaigrette.",
                "pris": round(kalorimål * 0.025, 1)
            },
            {
                "navn": "Fullkornsbrød med egg og tomat",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1605478371619-3b6b2b3b3b3b",
                "oppskrift": "Ristet brød med kokt egg, tomat og ruccola.",
                "pris": round(kalorimål * 0.02, 1)
            }
        ],
        "Middag": [
            {
                "navn": "Laks med grønnsaker",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1604908177522-4021d3a1e7d3",
                "oppskrift": "Ovnsbakt laks med brokkoli og søtpotet.",
                "pris": round(kalorimål * 0.03, 1)
            },
            {
                "navn": "Vegetargryte med linser",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
                "oppskrift": "Linser, tomat, paprika og krydder kokt i grønnsakskraft.",
                "pris": round(kalorimål * 0.022, 1)
            }
        ],
        "Kveldsmat": [
            {
                "navn": "Tunfiskwrap",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1613145993481-1b6b2b3b3b3b",
                "oppskrift": "Fullkornswrap med tunfisk, salat og lett dressing.",
                "pris": round(kalorimål * 0.019, 1)
            },
            {
                "navn": "Yoghurt med nøtter og honning",
                "kalorier": int(kalorimål),
                "bilde_url": "https://images.unsplash.com/photo-1625947202042-1b6b2b3b3b3b",
                "oppskrift": "Gresk yoghurt med valnøtter og honning.",
                "pris": round(kalorimål * 0.017, 1)
            }
        ]
    }

    return random.choice(forslag.get(kategori, []))
