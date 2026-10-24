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