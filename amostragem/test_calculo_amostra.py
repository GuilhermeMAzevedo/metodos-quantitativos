import pytest
import calculo_amostra as ca


def test_margem_conhecida():
    assert 100 * ca.margem_erro(2007) == pytest.approx(2.19, abs=0.01)


def test_tamanho_classico():
    assert ca.tamanho_amostra(0.05) == 385


def test_correcao_populacao_finita():
    assert ca.tamanho_amostra(0.05, N=1000) == 278


def test_ajuste_nao_resposta():
    assert ca.ajustar_nao_resposta(385, 0.8) == 482


def test_limites_nao_resposta():
    assert ca.limites_nao_resposta(0.5, 80, 100) == pytest.approx((0.4, 0.6))
    
def test_cenario_igual_ao_observado():
    assert ca.prevalencia_cenario(0.375, 793, 1040, 1) == pytest.approx(0.375)


def test_diferenca_proporcoes():
    dif, z, (li, ls) = ca.diferenca_proporcoes(0.5, 100, 0.5, 100)
    assert dif == 0 and z == 0 and li == pytest.approx(-ls)


def test_alocacao_soma_n():
    aloc = ca.alocacao_proporcional(577, ca.ESTRATOS_CE)
    assert sum(aloc.values()) == 577
    assert aloc["Fortaleza"] == 159
