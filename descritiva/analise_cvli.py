import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

os.makedirs("figuras", exist_ok=True)
os.makedirs("saidas", exist_ok=True)
plt.rcParams["figure.dpi"] = 120

df = pd.read_excel("data/CVLI_2009-a-2025.xlsx", sheet_name="CVLI")

df["Idade da Vítima"] = pd.to_numeric(df["Idade da Vítima"], errors="coerce")
df["Hora_num"] = pd.to_datetime(df["Hora"], format="%H:%M:%S").dt.hour
df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month
df["AnoMes"] = df["Data"].dt.to_period("M")