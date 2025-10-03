import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from supabase_klient import hent_unike_brukere, hent_vektlogg_db, hent_brukerinfo, test_tilkobling

st.set_page_config(page_title="Adminpanel", page_icon="🔒")
st.title("🔒 Adminpanel")
st.caption("Kun for administratorer")

# 🔐 Passordbeskyttelse
passord = st.text_input("Adminpassord", type="password")
if passord != st.secrets.get("ADMIN_PASSORD", ""):
    st.warning("⛔ Feil passord eller mangler tilgang.")
    st.stop()

# ✅ Supabase-test
if not test_tilkobling():
    st.error("❌ Klarte ikke å koble til Supabase")
    st.stop()

# 👥 Brukeroversikt
brukere = hent_unike_brukere()
st.write(f"Totalt antall brukere: **{len(brukere)}**")

# 📊 Aggregert statistikk
statistikk = []
for bruker_id in brukere:
    info = hent_brukerinfo(bruker_id)
    logg = hent_vektlogg_db(bruker_id)

    if not info or not logg:
        continue

    startvekt = info.get("startvekt")
    målvekt = info.get("målvekt")
    if not startvekt or not målvekt or startvekt <= målvekt:
        continue

    siste_vekt = logg[-1]["vekt"]
    fremdrift = round((startvekt - siste_vekt) / (startvekt - målvekt) * 100, 1)
    statistikk.append({
        "Bruker": bruker_id,
        "Startvekt": startvekt,
        "Siste vekt": siste_vekt,
        "Målvekt": målvekt,
        "Fremdrift (%)": fremdrift
    })

df_stat = pd.DataFrame(statistikk)

# 📈 Fremdriftstabell
if not df_stat.empty:
    st.write("### Fremdrift per bruker")
    st.dataframe(df_stat)

    # 🔥 Heatmap
    st.write("### Fremdrift heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df_stat[["Fremdrift (%)"]].T, annot=True, cmap="YlGnBu", cbar=False, fmt=".1f")
    st.pyplot(fig)

    # 📤 CSV-eksport
    csv = df_stat.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Last ned CSV", data=csv, file_name="fremdrift.csv", mime="text/csv")
else:
    st.info("Ingen brukere med registrert fremdrift.")

# 🔍 Detaljvisning med dato-filter
st.write("---")
valgt = st.selectbox("Velg bruker for detaljvisning", brukere)
if valgt:
    info = hent_brukerinfo(valgt)
    st.write("### Profilinformasjon")
    st.json(info)

    data = hent_vektlogg_db(valgt)
    df = pd.DataFrame(data)

    if not df.empty:
        df["dato"] = pd.to_datetime(df["dato"])
        df = df.rename(columns={"dato": "Dato", "vekt": "Vekt"})

        # 📅 Dato-filter
        dato_start = st.date_input("Fra dato", value=df["Dato"].min())
        dato_slutt = st.date_input("Til dato", value=df["Dato"].max())
        df_filtered = df[(df["Dato"] >= pd.to_datetime(dato_start)) & (df["Dato"] <= pd.to_datetime(dato_slutt))]

        st.line_chart(df_filtered.set_index("Dato")["Vekt"])
        st.write(df_filtered.tail())
    else:
        st.info("Ingen vektdata registrert for denne brukeren.")
