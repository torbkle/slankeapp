import random
from datetime import date
from supabase_klient import supabase
import streamlit as st
from oppskrift_api import generer_oppskrift

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
        oppskrift = generer_oppskrift(kategori, kcal)
        oppskrift["kategori"] = kategori
        plan.append(oppskrift)
        total += oppskrift["kalorier"]
    return plan, total

def vis_maltider(bruker_id):
    try:
        response = supabase.table("måltider")\
            .select("tidspunkt, kategori, kalorier")\
            .eq("bruker_id", bruker_id)\
            .order("tidspunkt", desc=True)\
            .execute()
        if response.data:
            for måltid in response.data:
                st.write(f"🍽️ {måltid['kategori']} – {måltid['kalorier']} kcal ({måltid['tidspunkt']})")
        else:
            st.info("Ingen måltider registrert enda.")
    except Exception as e:
        st.error(f"Feil ved henting av måltider: {e}")

def registrer_maltid(bruker_id):
    kategori = st.selectbox("Velg måltidstype", ["Frokost", "Lunsj", "Middag", "Kveldsmat"])
    kalorier = st.number_input("Kalorier", min_value=0, max_value=2000, step=10)
    if st.button("Lagre måltid"):
        try:
            supabase.table("måltider").insert({
                "bruker_id": bruker_id,
                "kategori": kategori,
                "kalorier": kalorier,
                "tidspunkt": str(date.today())
            }).execute()
            st.success("Måltid lagret!")
        except Exception as e:
            st.error(f"Feil ved lagring: {e}")

