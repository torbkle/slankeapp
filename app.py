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

# 🔐 Session state
if "innlogget" not in st.session_state:
    st.session_state["innlogget"] = False
if "bruker_id" not in st.session_state:
    st.session_state["bruker_id"] = ""

# 🧭 Innlogging
st.title("Slankeapp 🍽️")
st.caption("Din enkle kaloriguide for vektnedgang og vektlogg.")

eksisterende_brukere = hent_unike_brukere()
valgt_bruker = st.selectbox("Velg eksisterende bruker", eksisterende_brukere)
ny_bruker = st.text_input("Eller skriv inn nytt brukernavn")

if st.button("Logg inn"):
    bruker_id = ny_bruker if ny_bruker else valgt_bruker
    if bruker_id:
        st.session_state["innlogget"] = True
        st.session_state["bruker_id"] = bruker_id
        st.success(f"✅ Logget inn som: {bruker_id}")
    else:
        st.warning("Skriv inn brukernavn før du logger inn.")

# 🧩 Hovedinnhold
if st.session_state["innlogget"]:
    bruker_id = st.session_state["bruker_id"]
    st.success(f"✅ Innlogget som: {bruker_id}")

    if test_tilkobling():
        st.success("✅ Supabase-tilkobling aktiv")
    else:
        st.error("❌ Klarte ikke å koble til Supabase")

    info = hent_brukerinfo(bruker_id) or {}

    # 🧍 Personlig info
    st.write("### Personlig informasjon")
    kjønn = st.radio("Kjønn", ["Mann", "Kvinne"], index=0 if info.get("kjønn") != "Kvinne" else 1)
    alder = st.number_input("Alder", min_value=10, max_value=100, step=1, value=int(info.get("alder", 30)))
    høyde = st.number_input("Høyde (cm)", min_value=120.0, max_value=220.0, step=0.5, value=float(info.get("høyde", 175.0)))
    startvekt = st.number_input("Startvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, value=float(info.get("startvekt", 90.0)))
    målvekt = st.number_input("Målvekt (kg)", min_value=40.0, max_value=200.0, step=0.1, value=float(info.get("målvekt", 80.0)))

    if st.button("Oppdater profil"):
        lagre_brukerinfo({
            "bruker_id": bruker_id,
            "kjønn": kjønn,
            "alder": alder,
            "høyde": høyde,
            "startvekt": startvekt,
            "målvekt": målvekt
        })
        st.success("✅ Profil lagret")

    # 🔢 BMR og TDEE
    def beregn_bmr(vekt, høyde, alder, kjønn):
        return 10 * vekt + 6.25 * høyde - 5 * alder + (5 if kjønn == "Mann" else -161)

    bmr = beregn_bmr(startvekt, høyde, alder, kjønn)
    tdee = bmr * 1.4
    anbefalt_kalorimål = int(tdee - 500)
    st.write(f"🧮 BMR: {int(bmr)} kcal/dag")
    st.write(f"⚙️ TDEE: {int(tdee)} kcal/dag")
    st.write(f"🎯 Anbefalt kaloriinntak: {anbefalt_kalorimål} kcal/dag")

    # 🍽️ Måltidsplan
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

    # 🛠️ Adminvisning
    st.write("### 🛠️ Adminoversikt")
    admin_data = []

    for bruker in eksisterende_brukere:
        logg = hent_vektlogg_db(bruker)
        info = hent_brukerinfo(bruker)
        if logg and info:
            df_bruker = pd.DataFrame(logg)
            if len(df_bruker) > 0:
                siste_vekt = df_bruker["vekt"].iloc[-1]
                startvekt = info.get("startvekt", 0)
                målvekt = info.get("målvekt", 0)
    # 🛠️ Adminoversikt
    st.write("### 🛠️ Adminoversikt")
    admin_data = []

    for bruker in eksisterende_brukere:
        logg = hent_vektlogg_db(bruker)
        info = hent_brukerinfo(bruker)
        if logg and info:
            df_bruker = pd.DataFrame(logg)
            if len(df_bruker) > 0:
                siste_vekt = df_bruker["vekt"].iloc[-1]
                startvekt = float(info.get("startvekt", 0))
                målvekt = float(info.get("målvekt", 0))
                fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1) if startvekt > målvekt else 0
                admin_data.append({
                    "Bruker": bruker,
                    "Siste vekt": siste_vekt,
                    "Startvekt": startvekt,
                    "Målvekt": målvekt,
                    "Fremdrift (%)": fremdrift
                })
    
    if admin_data:
        st.dataframe(pd.DataFrame(admin_data))
    else:
        st.info("Ingen brukere med fullstendig data.")

