import pandas as pd
from datetime import datetime, timedelta

FILNAVN = "vektlogg.csv"

def registrer_vekt(dato, vekt):
    """
    Legger til ny vektregistrering i CSV-filen.
    """
    ny_rad = pd.DataFrame({"Dato": [dato], "Vekt": [vekt]})
    try:
        eksisterende = pd.read_csv(FILNAVN)
        df = pd.concat([eksisterende, ny_rad], ignore_index=True)
    except FileNotFoundError:
        df = ny_rad
    df.to_csv(FILNAVN, index=False)

def hent_vektlogg():
    """
    Leser vektdata fra CSV og returnerer som DataFrame.
    """
    try:
        df = pd.read_csv(FILNAVN)
        df["Dato"] = pd.to_datetime(df["Dato"])
        return df.sort_values("Dato")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Dato", "Vekt"])

def beregn_fremdrift(startvekt, målvekt, df):
    """
    Returnerer prosentvis fremdrift mot målvekten.
    """
    if df.empty:
        return 0, None

    siste_vekt = df["Vekt"].iloc[-1]
    total_tap = startvekt - målvekt
    faktisk_tap = startvekt - siste_vekt
    fremdrift = max(0, min(100, (faktisk_tap / total_tap) * 100))
    return round(fremdrift, 1), siste_vekt

def estimer_tid_til_mål(startvekt, målvekt, df):
    """
    Estimerer antall dager og dato til målvekt basert på gjennomsnittlig vekttap per dag.
    """
    if df.shape[0] < 2:
        return None, None  # Ikke nok data

    df = df.sort_values("Dato")
    dager = (df["Dato"].iloc[-1] - df["Dato"].iloc[0]).days
    vekttap = df["Vekt"].iloc[0] - df["Vekt"].iloc[-1]

    if dager == 0 or vekttap <= 0:
        return None, None  # Ingen fremgang

    tap_per_dag = vekttap / dager
    gjenstående = df["Vekt"].iloc[-1] - målvekt
    estimerte_dager = int(gjenstående / tap_per_dag)
    måldato = df["Dato"].iloc[-1] + timedelta(days=estimerte_dager)

    return estimerte_dager, måldato.date()
