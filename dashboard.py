import streamlit as st
import pandas as pd
import altair as alt
from supabase_klient import supabase
from auth import krever_innlogging
from branding import vis_logo, vis_footer

krever_innlogging()
vis_logo()
st.title("📈 Din helseoversikt")

bruker_id = st.session_state["bruker_id"]

# Vektgraf
st.subheader("📏 Vektutvikling")
try:
    vektdata = supabase.table("vektlogg").select("*").eq("bruker_id", bruker_id).order("dato").execute().data
    df = pd.DataFrame(vektdata)
    if not df.empty:
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="dato:T",
            y="vekt:Q"
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Ingen vektdata registrert ennå.")
except Exception as e:
    st.error(f"Feil ved henting av vektdata: {e}")

# Måltidsoversikt
st.subheader("🍽️ Kalorier siste 7 dager")
try:
    maltider = supabase.table("måltider").select("*").eq("bruker_id", bruker_id).order("tidspunkt", desc=True).limit(100).execute().data
    df_mat = pd.DataFrame(maltider)
    if not df_mat.empty:
        df_mat["dato"] = pd.to_datetime(df_mat["tidspunkt"]).dt.date
        kalorier_per_dag = df_mat.groupby("dato")["kalorier"].sum().reset_index()
        chart = alt.Chart(kalorier_per_dag).mark_bar().encode(
            x="dato:T",
            y="kalorier:Q"
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Ingen måltider registrert.")
except Exception as e:
    st.error(f"Feil ved henting av måltider: {e}")

vis_footer()
