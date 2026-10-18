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

def tabela_frequencia(coluna, nome):
    freq = df[coluna].value_counts(dropna=False)
    perc = ((freq / len(df)) * 100).round(2)
    tab = pd.DataFrame({"Frequência": freq, "Percentual (%)": perc})
    tab.to_csv(f"saidas/freq_{nome}.csv", sep=";", encoding="utf-8-sig")
    return tab

variaveis_freq = {
    "Natureza":"natureza",
    "Meio Empregado":"meio_empregado",
    "Gênero":"genero",
    "Escolaridade da Vítima":"escolaridade",
    "Raça da Vítima":"raca",
    "Dia da Semana":"dia_semana"
}

tabelas_freq = {nome: tabela_frequencia(col, nome) for col, nome in variaveis_freq.items()}

for nome, tab in tabelas_freq.items():
    print(f"\n=== {nome} ===\n{tab}")