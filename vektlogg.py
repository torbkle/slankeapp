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
