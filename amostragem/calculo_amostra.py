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

def prevalencia_cenario(p_obs, respondentes, elegiveis, razao):
    nao_resp = elegiveis - respondentes
    return p_obs * (respondentes + razao * nao_resp) / elegiveis


def diferenca_proporcoes(p1, n1, p2, n2, confianca=0.95, deff=1.0):
    dif = p2 - p1
    erro_padrao = sqrt(deff * (p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2))
    margem = z_critico(confianca) * erro_padrao
    return dif, dif / erro_padrao, (dif - margem, dif + margem)


def alocacao_proporcional(n, tamanhos):
    total = sum(tamanhos.values())
    cotas = {estrato: n * tam / total for estrato, tam in tamanhos.items()}
    alocacao = {estrato: int(cota) for estrato, cota in cotas.items()}
    sobra = n - sum(alocacao.values())
    for estrato in sorted(cotas, key=lambda e: cotas[e] - alocacao[e], reverse=True)[:sobra]:
        alocacao[estrato] += 1
    return alocacao


INDICADORES = [
    ("Qualquer violência", 0.375, 21_458_206),
    ("Ofensa verbal", 0.314, 17_714_721),
    ("Batida, empurrão ou chute", 0.169, 8_979_053),
    ("Perseguição", 0.161, 8_517_096),
    ("Ofensa sexual", 0.107, 5_381_783),
    ("Esfaqueamento ou tiro", 0.014, 350_854),
    ("Qualquer assédio", 0.496, 29_010_850),
]

ESTRATOS_CE = {"Fortaleza": 2_428_708, "Demais municípios da RMF": 1_477_183, "Interior": 4_889_066}

if __name__ == "__main__":
    print("1) Margens de erro (amostra aleatória simples, 95%, p = 0,5):")
    for rotulo, n, divulgada in [("Amostra nacional", 2007, 2.0),
                                 ("Mulheres entrevistadas", 1040, None),
                                 ("Módulo de autopreenchimento", 793, 3.0)]:
        calc = 100 * margem_erro(n)
        texto = f"divulgada {divulgada:.1f}" if divulgada else "sem margem divulgada"
        print(f"  {rotulo:28} n={n:5}  calculada {calc:.2f} pp  ({texto})")
    for deff in (1.5, 2.0):
        print(f"  Módulo com efeito de desenho {deff}: {100 * margem_erro(793, deff=deff):.2f} pp")

    print("\n2) Não resposta no módulo:")
    for ano, resp, eleg, p in [(2023, 818, 1042, 0.289), (2025, 793, 1040, 0.375)]:
        inf, sup = limites_nao_resposta(p, resp, eleg)
        print(f"  {ano}: {eleg - resp} de {eleg} ({100 * (eleg - resp) / eleg:.1f}%); "
              f"{100 * p:.1f}% com limites de pior caso de {100 * inf:.1f}% a {100 * sup:.1f}%")
    for razao in (0.5, 1.5):
        print(f"  2025 com não respondentes a {razao}x a prevalência: "
              f"{100 * prevalencia_cenario(0.375, 793, 1040, razao):.1f}%")

    print("\n3) Base populacional implícita em cada projeção:")
    for nome, p, projecao in INDICADORES:
        variavel = populacao_implicita(projecao, p, 793) / 1e6
        fixa = f"{projecao / (p - 0.03) / 1e6:.1f}" if p > 0.03 else "impossível"
        print(f"  {nome:26} {100 * p:5.1f}%  margem de cada p (n = 793): {variavel:.1f} mi"
              f"  |  margem fixa de 3,0 pp: {fixa}")

    print("\n4) Série histórica, 2023 (28,9%, n = 818) x 2025 (37,5%, n = 793):")
    for deff in (1.0, 2.0):
        dif, z, (li, ls) = diferenca_proporcoes(0.289, 818, 0.375, 793, deff=deff)
        print(f"  Efeito de desenho {deff}: +{100 * dif:.1f} pp, z = {z:.2f}, "
              f"IC 95% de {100 * li:.1f} a {100 * ls:.1f} pp")

    print("\n5) Proposta para o Ceará (±5 pp, 95%):")
    taxa = 793 / 1040
    for deff in (1.0, 1.5):
        n = tamanho_amostra(0.05, deff=deff)
        print(f"  Efeito de desenho {deff}: {n} respondentes, {ajustar_nao_resposta(n, taxa)} mulheres abordadas")
    for estrato, n_h in alocacao_proporcional(n, ESTRATOS_CE).items():
        print(f"  {estrato:25} {n_h:4} entrevistas  (margem no estrato {100 * margem_erro(n_h, deff=1.5):.1f} pp)")