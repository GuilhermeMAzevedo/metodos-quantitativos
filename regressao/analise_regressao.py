from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from preparar_ibge import normalizar

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
FIG = HERE / "figuras"
OUT = HERE / "saidas"

ANOS = (2021, 2023)      
USAR_LOG = True          
COL_Y = f"cvli_{ANOS[0]}_{ANOS[1]}"

plt.rcParams["figure.dpi"] = 120

def cvli_por_municipio(anos=ANOS):
    df = pd.read_excel(DATA / "CVLI_2009-a-2025.xlsx", sheet_name="CVLI")
    ano = df["Data"].dt.year
    y = (df[ano.between(*anos)]
         .groupby("Município").size()
         .reindex(df["Município"].unique(), fill_value=0)
         .rename(COL_Y)
         .reset_index())
    y.to_csv(DATA / "cvli_por_municipio.csv", sep=";", index=False, encoding="utf-8-sig")
    return y
