import random

# Måltidsdatabase med kategori, kalorier og prisestimat
MÅLTIDER = [
    {"navn": "Havregrøt med eple", "kategori": "Frokost", "kalorier": 300, "pris": 12, "oppskrift": "Kok havregryn med vann, topp med eplebiter."},
    {"navn": "Egg og knekkebrød", "kategori": "Frokost", "kalorier": 250, "pris": 10, "oppskrift": "Kokte egg med grovt knekkebrød og paprika."},
    {"navn": "Kyllingsalat", "kategori": "Lunsj", "kalorier": 450, "pris": 35, "oppskrift": "Grillet kylling, salat, couscous, dressing."},
    {"navn": "Tunfisksalat", "kategori": "Lunsj", "kalorier": 400, "pris": 25, "oppskrift": "Tunfisk, salat, mais og lett dressing."},
    {"navn": "Torsk med grønnsaker", "kategori": "Middag", "kalorier": 550, "pris": 40, "oppskrift": "Ovnsbakt torsk med brokkoli og gulrot."},
    {"navn": "Vegetargryte med linser", "kategori": "Middag", "kalorier": 500, "pris": 30, "oppskrift": "Linser, tomat, løk og krydder kokt sammen."},
    {"navn": "Gulrot og hummus", "kategori": "Snacks", "kalorier": 150, "pris": 8, "oppskrift": "Skjær gulrotstaver og dypp i hummus."},
    {"navn": "Cottage cheese med bær", "kategori": "Snacks", "kalorier": 350, "pris": 18, "oppskrift": "Bland cottage cheese med frosne bær."}
]

def generer_dagsplan(kalorimål):
    """
    Returnerer én frokost, én lunsj, én middag og én snack som til sammen nærmer seg kalorimålet.
    """
    plan = []
    total_kalorier = 0

    for kategori in ["Frokost", "Lunsj", "Middag", "Snacks"]:
        valg = [m for m in MÅLTIDER if m["kategori"] == kategori]
        måltid = random.choice(valg)
        plan.append(måltid)
        total_kalorier += måltid["kalorier"]

    return plan, total_kalorier

