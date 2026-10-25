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

def ler_pib(caminho, ano=ANO_PIB, uf=UF):
    abas = ler_abas(caminho)
    for bruto in abas:
        nomes = bruto.head(40).apply(lambda c: c.map(lambda x: normalizar(str(x))))
        linha_cab = next((i for i in range(len(nomes)) if (nomes.iloc[i] == "ano").any()), None)
        if linha_cab is not None:
            break
    else:
        raise ValueError(f"Não achei a linha de cabeçalho (coluna 'Ano') em {caminho.name}. "
                         f"Primeiras linhas da 1ª aba:\n{abas[0].head(8).to_string()}")
    cab = [normalizar(str(c)) for c in bruto.iloc[linha_cab]]
    dados = bruto.iloc[linha_cab + 1:].reset_index(drop=True)
    def posicao(*partes, exato=False):
        for i, nome in enumerate(cab):
            if (nome == partes[0]) if exato else all(p in nome for p in partes):
                return i
        raise ValueError(f"Coluna com {partes} não encontrada. Colunas lidas: {cab}")
 
    i_ano = posicao("ano", exato=True)
    i_uf = posicao("sigla", "unidade da federacao")
    i_mun = posicao("nome do municipio")
    i_pib = posicao("per capita")
 
    anos = dados.iloc[:, i_ano].map(para_numero)
    ufs = dados.iloc[:, i_uf].astype(str).str.strip().str.upper()
    sel = dados[(anos == ano) & (ufs == uf)]
    return pd.DataFrame({"municipio": sel.iloc[:, i_mun].astype(str).str.strip().values,
                         "pib_per_capita": sel.iloc[:, i_pib].map(para_numero).values})

def unir(pop, pib):
    pop = pop.assign(chave=pop["municipio"].map(normalizar))
    pib = pib.assign(chave=pib["municipio"].map(normalizar))
    problemas = []
    if len(pop) != N_MUNICIPIOS:
        problemas.append(f"população tem {len(pop)} municípios (esperado {N_MUNICIPIOS})")
    if len(pib) != N_MUNICIPIOS:
        problemas.append(f"PIB tem {len(pib)} municípios (esperado {N_MUNICIPIOS})")
    base = pop.merge(pib[["chave", "pib_per_capita"]], on="chave", how="inner", validate="one_to_one")
    if len(base) != N_MUNICIPIOS:
        so_pop = sorted(set(pop["chave"]) - set(pib["chave"]))
        so_pib = sorted(set(pib["chave"]) - set(pop["chave"]))
        problemas.append(f"{len(base)} casaram; só na população: {so_pop}; só no PIB: {so_pib}")
    if base["pib_per_capita"].isna().any():
        problemas.append("há municípios sem PIB per capita: " + str(base.loc[base["pib_per_capita"].isna(), "municipio"].tolist()))
    if problemas:
        raise ValueError("Problemas na junção:\n- " + "\n- ".join(problemas))
    return base[["municipio", "populacao", "pib_per_capita"]].sort_values("municipio")

def localizar(trecho):
    achados = [p for p in RAW.iterdir()
               if p.is_file() and trecho in p.name.lower() and p.suffix.lower() in EXTENSOES]
    if len(achados) != 1:
        raise FileNotFoundError(f"Esperava 1 arquivo com '{trecho}' no nome em {RAW}, achei {len(achados)}. "
                                f"Passe os caminhos como argumentos.")
    return achados[0]