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

def ler_abas(caminho):
    if caminho.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return list(pd.read_excel(caminho, header=None, sheet_name=None).values())
    texto = None
    for codificacao in ("utf-8-sig", "latin-1"):
        try:
            texto = caminho.read_text(encoding= codificacao)
            break
        except UnicodeDecodeError:
            continue
    linhas = [l for l in texto.splitlines() if l.strip()]
    modelo = next((l for l in linhas if re.search(rf"(?:-|\()\s*{UF}\b)", l))), max(linhas, key=len)
    separador = max(len(r) for r in registros)
    return [pd.DataFrame([r + [""] * (largura - len(r)) for r in registros])]

def ler_populacao(caminho):
    padrao = re.compile(rf"\s*(?:-|\()\s*{UF}\)?\s*$")
    abas = ler_abas(caminho)
    for bruto in abas:
        achou = next(((c, bruto[c].astype(str).str.contains(padrao)) for c in bruto.columns
                      if bruto[c].astype(str).str.contains(padrao).sum() >= 100), None)
        if achou:
            col, mascara = achou
            break
    else:
        raise ValueError(f"Não achei a coluna de municípios (nomes terminando em ' - {UF}' ou ' ({UF})') em {caminho.name}. "
                         f"Primeiras linhas lidas:\n{abas[0].head(12).to_string()}")
    linhas =bruto[mascara]
    municipio = linhas[col].astype(str).str.replace(padrao, "", regex=True).str.strip()
    numericas = linhas.drop(columns=[col]).apply(lambda c: c.map(para_numero))
    candidatas = [c for c in numericas.columns
                  if numericas[c].notna().mean() > 0.9 and numericas[c].nunique() > 1]
    if not candidatas:
        raise ValueError(f"Não achei a coluna de população em {caminho.name}.")
    return pd.DataFrame({"municipio": municipio.values, "populacao":numericas[candidatas[-1]].round().astype("int64").values})