import streamlit as st
from datetime import date
import pandas as pd
from måltidslogikk import generer_dagsplan, fordel_kalorier, beregn_bmr
from supabase_klient import (
    test_tilkobling,
    registrer_vekt_db,
    hent_vektlogg_db,
    hent_unike_brukere,
    lagre_brukerinfo,
    hent_brukerinfo
)
from style import css, ramme, seksjon, ikonlinje
from branding import vis_logo, INFERA_GRØNN

st.set_page_config(page_title="Slankeapp", page_icon="🥗", layout="centered")
css()
vis_logo()

# 🔐 Session state
if "innlogget" not in st.session_state:
    st.session_state["innlogget"] = False
if "bruker_id" not in st.session_state:
    st.session_state["bruker_id"] = ""

# 🧭 Innlogging
if not st.session_state["innlogget"]:
    ramme("🔐 Logg inn", "Velg eksisterende bruker eller opprett ny.")
    eksisterende_brukere = hent_unike_brukere()
    valgt_bruker = st.selectbox("👤 Velg bruker", eksisterende_brukere)
    ny_bruker = st.text_input("✍️ Ny bruker", placeholder="Skriv inn brukernavn")

    if st.button("🚪 Logg inn"):
        bruker_id = ny_bruker if ny_bruker else valgt_bruker
        if bruker_id:
            st.session_state["innlogget"] = True
            st.session_state["bruker_id"] = bruker_id
            st.rerun()
        else:
            st.warning("⚠️ Skriv inn brukernavn før du logger inn.")

# 🧩 Hovedinnhold
if st.session_state["innlogget"]:
    bruker_id = st.session_state["bruker_id"]
    seksjon(f"🍽️ Slankeapp – velkommen, {bruker_id}")

    if not test_tilkobling():
        st.error("❌ Klarte ikke å koble til Supabase")
        st.stop()

    info = hent_brukerinfo(bruker_id) or {}

    seksjon("👤 Profil")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            kjønn = st.radio("Kjønn", ["Mann", "Kvinne"], index=0 if info.get("kjønn") != "Kvinne" else 1)
            alder = st.number_input("Alder", min_value=10, max_value=100, value=int(info.get("alder", 30)))
            høyde = st.number_input("Høyde (cm)", min_value=120.0, max_value=220.0, value=float(info.get("høyde", 175.0)))
        with col2:
            startvekt = st.number_input("Startvekt (kg)", min_value=40.0, max_value=200.0, value=float(info.get("startvekt", 90.0)))
            målvekt = st.number_input("Målvekt (kg)", min_value=40.0, max_value=200.0, value=float(info.get("målvekt", 80.0)))

    if st.button("💾 Lagre profil"):
        lagre_brukerinfo({
            "bruker_id": bruker_id,
            "kjønn": kjønn,
            "alder": alder,
            "høyde": høyde,
            "startvekt": startvekt,
            "målvekt": målvekt
        })
        ikonlinje("Profil lagret")

    seksjon("🔢 Kaloriberegning")
    bmr = beregn_bmr(startvekt, høyde, alder, kjønn)
    tdee = bmr * 1.4
    anbefalt_kalorimål = int(tdee - 500)
    st.metric("BMR", f"{int(bmr)} kcal/dag")
    st.metric("TDEE", f"{int(tdee)} kcal/dag")
    st.metric("Anbefalt kaloriinntak", f"{anbefalt_kalorimål} kcal/dag")

    seksjon("🍽️ Måltidsplan")
    kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, anbefalt_kalorimål)
    fordeling = fordel_kalorier(kalorimål)
    st.dataframe(pd.DataFrame.from_dict(fordeling, orient="index", columns=["kcal"]))

    plan, total = generer_dagsplan(kalorimål)
    for måltid in plan:
        with st.expander(f"{måltid['kategori']} – {måltid['navn']} ({måltid['kalorier']} kcal)"):
            st.write(f"💰 Pris: ca. kr {måltid['pris']}")
            st.write(måltid["oppskrift"])
    st.write(f"**Totalt kalorier i dag:** {total} kcal")

    seksjon("📉 Vektlogg")
    dagens_vekt = st.number_input("Registrer dagens vekt (kg)", min_value=40.0, max_value=200.0)

    if st.button("📤 Lagre vekt"):
        registrer_vekt_db(bruker_id, str(date.today()), dagens_vekt)
        ikonlinje(f"Vekt {dagens_vekt} kg lagret for {date.today()}")

    data = hent_vektlogg_db(bruker_id)
    df = pd.DataFrame(data)

    if not df.empty:
        df["dato"] = pd.to_datetime(df["dato"])
        df = df.rename(columns={"dato": "Dato", "vekt": "Vekt"})
        st.line_chart(df.set_index("Dato")["Vekt"])
        st.dataframe(df.tail())

        if startvekt > målvekt:
            siste_vekt = df["Vekt"].iloc[-1]
            fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1)
            st.metric("Siste vekt", f"{siste_vekt} kg")
            st.metric("Fremdrift mot mål", f"{fremdrift}%")
            st.progress(fremdrift / 100)
        else:
            st.warning("Startvekten må være høyere enn målvekten for å vise fremdrift.")
    else:
        st.info("Ingen vektdata registrert ennå.")
