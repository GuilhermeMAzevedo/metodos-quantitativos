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