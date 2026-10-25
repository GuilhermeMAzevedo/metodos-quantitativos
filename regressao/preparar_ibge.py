import csv
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RAW = DATA / "raw"

UF = "CE"
ANO_PIB = 2022
N_MUNICIPIOS = 184
EXTENSOES = {".csv", ".txt", ".xlsx", ".xlsm", ".xls"}

def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower().strip()

def para_numero(valor):
    if isinstance(valor, (int, float, np.integer, np.floating)):
        return float(valor)
    s = str(valor).strip().replace("\u00a0", "").replace(" ", "")
    if not re.search(r"\d", s):
        return np.nan
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", ""). replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan
