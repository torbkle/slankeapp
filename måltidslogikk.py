import random

def beregn_bmr(vekt, høyde, alder, kjønn):
    return 10 * vekt + 6.25 * høyde - 5 * alder + (5 if kjønn == "Mann" else -161)

def fordel_kalorier(kalorimål):
    return {
        "Frokost": int(kalorimål * 0.25),
        "Lunsj": int(kalorimål * 0.30),
        "Middag": int(kalorimål * 0.35),
        "Kveldsmat": int(kalorimål * 0.10)
    }

def generer_dagsplan(kalorimål):
    fordeling = fordel_kalorier(kalorimål)
    plan = []
    total = 0

    for kategori, kcal in fordeling.items():
        måltid = {
            "kategori": kategori,
            "navn": random.choice(["Havregrøt", "Kyllingsalat", "Laks med grønnsaker", "Wrap med tunfisk"]),
            "kalorier": kcal,
            "pris": round(kcal * 0.02, 1),
            "oppskrift": f"En enkel oppskrift for {kategori} med ca. {kcal} kcal."
        }
        plan.append(måltid)
        total += kcal

    return plan, total
