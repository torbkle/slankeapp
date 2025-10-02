import random

# Enkle måltidsforslag med kalorier og oppskrift
MÅLTIDER = [
    {"navn": "Havregrøt med eple", "kalorier": 300, "oppskrift": "Kok havregryn med vann, topp med eplebiter."},
    {"navn": "Kyllingsalat", "kalorier": 450, "oppskrift": "Grillet kylling, salat, couscous, dressing."},
    {"navn": "Torsk med grønnsaker", "kalorier": 550, "oppskrift": "Ovnsbakt torsk med brokkoli og gulrot."},
    {"navn": "Cottage cheese med bær", "kalorier": 350, "oppskrift": "Bland cottage cheese med frosne bær."},
    {"navn": "Gulrot og hummus", "kalorier": 150, "oppskrift": "Skjær gulrotstaver og dypp i hummus."},
    {"navn": "Tunfisksalat", "kalorier": 400, "oppskrift": "Tunfisk, salat, mais og lett dressing."},
    {"navn": "Egg og knekkebrød", "kalorier": 250, "oppskrift": "Kokte egg med grovt knekkebrød og paprika."}
]

def generer_dagsplan(kalorimål):
    """
    Returnerer en liste med måltider som til sammen nærmer seg ønsket kalorimål.
    """
    valgt = []
    total = 0
    tilgjengelige = MÅLTIDER.copy()
    random.shuffle(tilgjengelige)

    for måltid in tilgjengelige:
        if total + måltid["kalorier"] <= kalorimål:
            valgt.append(måltid)
            total += måltid["kalorier"]

    return valgt
