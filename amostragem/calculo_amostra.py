from math import ceil, sqrt
from statistics import NormalDist


def z_critico(confianca=0.95):
    return NormalDist().inv_cdf(1 - (1 - confianca) / 2)


def margem_erro(n, p=0.5, confianca=0.95, deff=1.0):
    return z_critico(confianca) * sqrt(deff * p * (1 - p) / n)


def tamanho_amostra(margem, p=0.5, confianca=0.95, N=None, deff=1.0):
    n0 = deff * z_critico(confianca) ** 2 * p * (1 - p) / margem ** 2
    if N is not None:
        n0 = n0 / (1 + (n0 - 1) / N)
    return ceil(n0)


def ajustar_nao_resposta(n, taxa_resposta):
    return ceil(n / taxa_resposta)


def limites_nao_resposta(p_obs, respondentes, elegiveis):
    casos = p_obs * respondentes
    return casos / elegiveis, (casos + elegiveis - respondentes) / elegiveis


def populacao_implicita(projecao, p, n, confianca=0.95):
    return projecao / (p - margem_erro(n, p, confianca))
