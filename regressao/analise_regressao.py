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

def carregar_ibge():
    ibge = pd.read_csv(DATA / "ibge_ce.csv", sep=None, engine="python", encoding="utf-8-sig")
    esperadas = {"municipio", "populacao", "pib_per_capita"}
    faltando = esperadas - set(ibge.columns)
    if faltando:
        raise ValueError(f"ibge_ce.csv sem as colunas {sorted(faltando)}; colunas lidas: {list(ibge.columns)}")
    ibge["municipio"] = ibge["municipio"].astype(str).str.replace(r"\s*-\s*CE\s*$", "", regex=True)
    return ibge

def unir_bases(y, ibge):
    y = y.assign(chave=y["Município"].map(normalizar))
    ibge = ibge.assign(chave=ibge["municipio"].map(normalizar)).drop(columns="municipio")
    base = y.merge(ibge, on="chave", how="left", validate="one_to_one")
    sem_dado = base[base[["populacao", "pib_per_capita"]].isna().any(axis=1)]["Município"].tolist()
    if sem_dado:
        raise ValueError(f"{len(sem_dado)} municípios sem dado do IBGE: {sem_dado}")
    return base.drop(columns="chave")

def preparar_variaveis(base, usar_log=USAR_LOG):
    d = base.copy()
    if usar_log:
        d["y"] = np.log1p(d[COL_Y])
        d["x1"] = np.log(d["populacao"])
        d["x2"] = np.log(d["pib_per_capita"])
    else:
        d["y"], d["x1"], d["x2"] = d[COL_Y], d["populacao"], d["pib_per_capita"]
    return d

def rotulos(usar_log=USAR_LOG):
    pref = "log " if usar_log else ""
    return {"y": f"{pref}CVLI {ANOS[0]}-{ANOS[1]}", "x1": f"{pref}população (Censo 2022)",
            "x2": f"{pref}PIB per capita"}

def grafico_dispersao(d, x, arquivo, destacar="Fortaleza"):
    nomes = rotulos()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(d[x], d["y"], alpha=0.7)
    if destacar in set(d["Município"]):
        p = d[d["Município"] == destacar].iloc[0]
        ax.annotate(destacar, (p[x], p["y"]), textcoords="offset points", xytext=(-45, -3))
    ax.set_xlabel(nomes[x])
    ax.set_ylabel(nomes["y"])
    ax.set_title(f"{nomes['y']} × {nomes[x]}")
    plt.tight_layout()
    plt.savefig(FIG / f"{arquivo}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

def correlacoes(d):
    linhas = []
    for a, b in [("x1", "y"), ("x2", "y"), ("x1", "x2")]:
        r, p = stats.pearsonr(d[a], d[b])
        rho, p_s = stats.spearmanr(d[a], d[b])
        linhas.append({"par": f"{a} × {b}", "pearson_r": r, "p_pearson": p,
                       "spearman_rho": rho, "p_spearman": p_s})
    return pd.DataFrame(linhas)

def ajustar(formula, d):
    return smf.ols(formula, data=d).fit()

def calcular_vif(d, colunas=("x1", "x2")):
    X = sm.add_constant(d[list(colunas)])
    return pd.Series({c: variance_inflation_factor(X.values, i + 1) for i, c in enumerate(colunas)}, name="VIF")

def anova_modelo(m):
    tabela = sm.stats.anova_lm(m, typ=2)
    return tabela, m.fvalue, m.f_pvalue

def diagnostico_residuos(m, d):
    res = m.resid
    w, p_sw = stats.shapiro(res)
    _, p_bp, _, _ = het_breuschpagan(res, m.model.exog)
    cook = pd.Series(m.get_influence().cooks_distance[0], index=d.index)
    top = d.loc[cook.nlargest(5).index, ["Município"]].assign(cook=cook.nlargest(5))
    return {"shapiro_W": w, "shapiro_p": p_sw, "breusch_pagan_p": p_bp, "cook_top5": top}

def grafico_residuos(m, arquivo):
    res = m.resid
    fig, eixos = plt.subplots(1, 3, figsize=(14, 4))
    sm.qqplot(res, line="s", ax=eixos[0])
    eixos[0].set_title("Q-Q dos resíduos")
    eixos[1].hist(res, bins=20)
    eixos[1].set_title("Histograma dos resíduos")
    eixos[2].scatter(m.fittedvalues, res, alpha=0.7)
    eixos[2].axhline(0, color="gray")
    eixos[2].set_xlabel("valores ajustados")
    eixos[2].set_ylabel("resíduos")
    eixos[2].set_title("Resíduos × ajustados")
    plt.tight_layout()
    plt.savefig(FIG / f"{arquivo}.pdf", bbox_inches="tight")
    plt.show()
    plt.close()

def prever(m, populacao, pib_per_capita, usar_log=USAR_LOG):
    novo = pd.DataFrame({"x1": [np.log(populacao) if usar_log else populacao],
                         "x2": [np.log(pib_per_capita) if usar_log else pib_per_capita]})
    q = m.get_prediction(novo).summary_frame(alpha=0.05)
    if usar_log:
        q = q.assign(casos_previstos=np.expm1(q["mean"]),
                     casos_ic_inf=np.expm1(q["obs_ci_lower"]),
                     casos_ic_sup=np.expm1(q["obs_ci_upper"]))
    return q