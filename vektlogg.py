from supabase_klient import registrer_vekt_db, hent_vektlogg_db
import pandas as pd

# Midlertidig bruker-ID (kan utvides med innlogging senere)
bruker_id = "demo"

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
else:
    st.info("Ingen vektdata registrert ennå.")
