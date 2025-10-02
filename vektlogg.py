import pandas as pd
import os

FILNAVN = "vektlogg.csv"

def registrer_vekt(dato, vekt):
    """
    Legger til ny vektregistrering i CSV-filen.
    """
    ny_rad = pd.DataFrame({"Dato": [dato], "Vekt": [vekt]})
    if os.path.exists(FILNAVN):
        df = pd.read_csv(FILNAVN)
        df = pd.concat([df, ny_rad], ignore_index=True)
    else:
        df = ny_rad
    df.to_csv(FILNAVN, index=False)

def hent_vektlogg():
    """
    Returnerer hele vektloggen som DataFrame.
    """
    if os.path.exists(FILNAVN):
        return pd.read_csv(FILNAVN)
    else:
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
