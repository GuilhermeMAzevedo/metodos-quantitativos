# Métodos Quantitativos em Computação

![Python](https://img.shields.io/badge/python-3.12-blue) ![Relatórios](https://img.shields.io/badge/relatórios-LaTeX-green)

Trabalhos da disciplina **Métodos Quantitativos em Computação** (Ciência da Computação — Universidade de Fortaleza, 2026). A análise é feita em Python e os relatórios são escritos em LaTeX, com foco em dados reais de segurança pública do Ceará.

## Trabalhos

| Trabalho | Tema | Código | Relatório | Status |
|---|---|---|---|---|
| AV1 | Estatística descritiva dos CVLI no Ceará (2009–2025) | [`analise_cvli.py`](descritiva/analise_cvli.py) | [PDF](descritiva/relatorio_descritiva.pdf) | concluído |
| AV2 | Regressão linear: CVLI por município × população e PIB per capita | [`analise_regressao.py`](regressao/analise_regressao.py) | — | em andamento |
| AV3 | Estimação e amostragem | — | — | em breve |

## Resultados

### AV1 — Estatística descritiva

Análise de 59.340 registros de CVLI (um por vítima) em 184 municípios, de 2009 a 2025:

- A série anual sobe até o pico de **5.133 casos em 2017** e cai a partir de 2018 (3.021 em 2025).
- **92,3%** das vítimas são homens; a mediana de idade é **27 anos** e a moda, 20.
- **Arma de fogo** em 83,5% dos casos.
- Sábado e domingo concentram cerca de **36%** das ocorrências, com pico à noite.
- Limitação da base: raça/cor não informada em 77,7% dos registros.

Inclui séries de frequência, tabelas cruzadas, gráficos de setor, barras e linha, medidas de posição e dispersão e boxplot da idade.

### AV2 — Regressão linear

Em andamento: regressão do total de CVLI por município (2021–2023) em função da população (Censo 2022) e do PIB per capita (IBGE), com diagnóstico de resíduos, ANOVA e previsões.

## Estrutura

```
metodos-quantitativos/
├── data/                  # bases (SSPDS/CE e IBGE) e documentação das fontes
│   └── raw/               # arquivos brutos do IBGE, sem edição
├── descritiva/            # analise_cvli.py, relatorio_descritiva.tex/.pdf, figuras/
├── regressao/             # analise_regressao.py, preparar_ibge.py, figuras/
├── requirements.txt
└── README.md
```

O trabalho de amostragem entra em `amostragem/` quando for concluído.

## Como executar

```bash
git clone https://github.com/GuilhermeMAzevedo/metodos-quantitativos.git
cd metodos-quantitativos

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS
pip install -r requirements.txt

python descritiva/analise_cvli.py
python regressao/analise_regressao.py     # usa data/ibge_ce.csv, que já está no repositório
```

Os scripts usam caminhos relativos ao próprio arquivo (podem ser executados de qualquer pasta) e leem as bases em `data/`. Eles abrem os gráficos com `plt.show()` (feche cada janela para continuar) e salvam os PDFs em `figuras/` e os arquivos de apoio em `saidas/`, dentro da pasta de cada trabalho. A pasta `saidas/` é ignorada pelo Git.

Para regerar `data/ibge_ce.csv` a partir dos arquivos brutos do IBGE, veja `data/README.md` e execute `python regressao/preparar_ibge.py`.

### Compilar o relatório

Use o Overleaf com o compilador **pdfLaTeX**, ou localmente:

```bash
cd descritiva
pdflatex relatorio_descritiva.tex
pdflatex relatorio_descritiva.tex     # segunda passada para o sumário
```

É preciso uma instalação completa do TeX Live (pacotes `babel` em português, `booktabs`, `multirow`, `makecell`, `listings`, `xurl`).

## Dados

Todas as bases são públicas: CVLI da SSPDS/CE e, no AV2, população e PIB municipais do IBGE. Fontes, colunas e limitações em [`data/README.md`](data/README.md).

## Tecnologias

Python · pandas · matplotlib · statsmodels · SciPy · LaTeX

## Autoria

Desenvolvido por [Guilherme Azevedo](https://github.com/GuilhermeMAzevedo).