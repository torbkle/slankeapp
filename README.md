# 🥗 Slankeapp

Slankeapp er en enkel kaloriguide og vektlogg bygget med Streamlit og Supabase. Den hjelper deg med å planlegge måltider, følge fremdrift og lagre data i skyen.

## 🚀 Funksjoner

- Dynamisk innlogging med personlig bruker-ID
- Automatisk lagring og henting av:
  - Vektdata
  - Personlig informasjon (kjønn, alder, høyde, startvekt, målvekt)
- Beregning av BMR og TDEE
- Måltidsplan med kalorifordeling
- Fremdriftsvisning og mini-dashboard
- Supabase-integrasjon med sikker skybasert lagring

## 🛠️ Teknologi

- [Streamlit](https://streamlit.io/)
- [Supabase](https://supabase.com/)
- Python, Pandas

## 📦 Installasjon

```bash
git clone https://github.com/torbkle/slankeapp.git
cd slankeapp
pip install -r requirements.txt
streamlit run app.py
