import streamlit as st
from datetime import date
import pandas as pd
from måltidslogikk import generer_dagsplan, fordel_kalorier
from supabase_klient import (
    test_tilkobling,
    registrer_vekt_db,
    hent_vektlogg_db,
    hent_unike_brukere,
    lagre_brukerinfo,
    hent_brukerinfo
)

st.set_page_config(page_title="Slankeapp", page_icon="🍽️")

# 🔐 Innlogging
st.title("Slankeapp 🍽️")
st.caption("Din enkle kaloriguide for vektnedgang og måltidsplanlegging.")

st.write("### Logg inn")
eksisterende_brukere = hent_unike_brukere()
valgt_bruker = st.selectbox("Velg eksisterende bruker", eksisterende_brukere)
ny_bruker = st.text_input("Eller skriv inn nytt brukernavn")
bruker_id = ny_bruker if ny_bruker else valgt_bruker
logg_inn = st.button("Logg inn")

if logg_inn and bruker_id:
    st.success(f"✅ Logget inn som: {bruker_id}")

    # 🔌 Supabase-status
    if test_tilkobling():
        st.success("✅ Supabase-tilkobling aktiv")
    else:
        st.error("❌ Klarte ikke å koble til Supabase – sjekk Secrets eller tabellstruktur")

    # 🧍 Personlig informasjon
    st.write("### Personlig informasjon")
    info = hent_brukerinfo(bruker_id)
    kjønn = st.radio("Kjønn", ["Mann", "Kvinne"], index=0 if not info else ["Mann", "Kvinne"].index(info["kjønn"]))
    alder = st.number_input("Alder", min_value=10, max_value=100, step=1, value=info["alder"] if info else 30)
    høyde = st.number_input("Høyde (cm)", min_value=120.0, max_value=220.0, step=0.5, value=info["høyde"] if info else 175.0)

    # 🎯 Vektmål
    st.write("### Vektmål")
    startvekt = st.number_input("Startvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, value=info["startvekt"] if info else 90.0)
    målvekt = st.number_input("Målvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, value=info["målvekt"] if info else 80.0)

    # 💾 Lagre brukerinfo
    if st.button("Oppdater profil"):
        brukerdata = {
            "bruker_id": bruker_id,
            "kjønn": kjønn,
            "alder": alder,
            "høyde": høyde,
            "startvekt": startvekt,
            "målvekt": målvekt
        }
        lagre_brukerinfo(brukerdata)
        st.success("✅ Profil lagret")

    # 🔢 BMR og TDEE
    def beregn_bmr(vekt, høyde, alder, kjønn):
        if kjønn == "Mann":
            return 10 * vekt + 6.25 * høyde - 5 * alder + 5
        else:
            return 10 * vekt + 6.25 * høyde - 5 * alder - 161

    bmr = beregn_bmr(startvekt, høyde, alder, kjønn)
    tdee = bmr * 1.4
    anbefalt_kalorimål = int(tdee - 500)
    st.write(f"🧮 BMR: {int(bmr)} kcal/dag")
    st.write(f"⚙️ TDEE: {int(tdee)} kcal/dag")
    st.write(f"🎯 Anbefalt kaloriinntak: {anbefalt_kalorimål} kcal/dag")

    # 🍽️ Kalorimål og måltidsplan
    kalorimål = st.slider("Velg daglig kaloriinntak", 1200, 2500, anbefalt_kalorimål)
    fordeling = fordel_kalorier(kalorimål)
    st.write("### Kalorifordeling per måltid")
    for kategori, kcal in fordeling.items():
        st.write(f"{kategori}: {kcal} kcal")

    plan, total = generer_dagsplan(kalorimål)
    st.write("### Dagens måltidsforslag")
    for måltid in plan:
        st.markdown(f"**{måltid['kategori']} – {måltid['navn']}**")
        st.write(f"{måltid['kalorier']} kcal – ca. kr {måltid['pris']}")
        st.write(måltid["oppskrift"])
        st.divider()
    st.write(f"**Totalt kalorier i dag:** {total} kcal")

    # 📉 Vektlogg
    st.write("### Vektlogg")
    dagens_vekt = st.number_input("Registrer dagens vekt (kg)", min_value=40.0, max_value=200.0, step=0.1)

    if st.button("Lagre vekt"):
        registrer_vekt_db(bruker_id, str(date.today()), dagens_vekt)
        st.success(f"Vekt {dagens_vekt} kg lagret for {date.today()}")

    # 🔍 Testvisning av vektdata
    st.write(f"🔍 Bruker-ID: {bruker_id}")
    st.write(f"📦 Vektdata: {hent_vektlogg_db(bruker_id)}")

    data = hent_vektlogg_db(bruker_id)
    df = pd.DataFrame(data)

    if not df.empty:
        df["dato"] = pd.to_datetime(df["dato"])
        df = df.rename(columns={"dato": "Dato", "vekt": "Vekt"})
        st.line_chart(df.set_index("Dato")["Vekt"])
        st.write(df.tail())

        if startvekt > målvekt:
            siste_vekt = df["Vekt"].iloc[-1]
            fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1)
            st.write(f"**Siste registrerte vekt:** {siste_vekt} kg")
            st.write(f"**Målvekt:** {målvekt} kg")
            st.progress(fremdrift / 100)
            st.write(f"**Fremdrift mot mål:** {fremdrift}%")
        else:
            st.warning("Startvekten må være høyere enn målvekten for å vise fremdrift.")
    else:
        st.info("Ingen vektdata registrert ennå.")

    # 📊 Mini-dashboard
    st.write("### 📊 Fremdrift for alle brukere")
    total_fremdrift = 0
    gyldige_brukere = 0

    for bruker in eksisterende_brukere:
        logg = hent_vektlogg_db(bruker)
        if logg:
            df_bruker = pd.DataFrame(logg)
            if "vekt" in df_bruker.columns and len(df_bruker) > 1:
                start = df_bruker["vekt"].iloc[0]
                slutt = df_bruker["vekt"].iloc[-1]
                if start > slutt:
                    fremdrift = (start - slutt) / start * 100
                    total_fremdrift += fremdrift
                    gyldige_brukere += 1

    if gyldige_brukere > 0:
        gjennomsnitt = round(total_fremdrift / gyldige_brukere, 1)
        st.metric("Gjennomsnittlig fremdrift", f"{gjennomsnitt}%")
    else:
        st.info("Ingen brukere med gyldig fremdrift registrert ennå.")

else:
    st.info("Skriv inn brukernavn og trykk 'Logg inn' for å starte.")
