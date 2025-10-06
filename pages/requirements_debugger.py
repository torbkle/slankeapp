import streamlit as st

st.set_page_config(page_title="Pakkeoversikt", layout="centered")
st.title("📦 Pakkeoversikt – Slankeapp")

# 📋 Liste over nødvendige pakker
pakker = {
    "streamlit": "UI og frontend",
    "pandas": "Databehandling",
    "seaborn": "Visualisering",
    "matplotlib": "Plotting",
    "supabase": "Supabase-klient",
    "python-dotenv": ".env-håndtering",
    "requests": "REST-kall til Supabase Admin API"
}

# 🔍 Sjekk om hver pakke er installert
for navn, beskrivelse in pakker.items():
    try:
        __import__(navn)
        st.success(f"✅ `{navn}` er installert – {beskrivelse}")
    except ImportError:
        st.error(f"🚫 `{navn}` mangler – {beskrivelse}")

st.markdown("---")
st.info("Hvis du kjører på Streamlit Cloud, må alle disse pakkene være oppført i `requirements.txt`.")
