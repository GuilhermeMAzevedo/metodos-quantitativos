# Métodos Quantitativos em Computação

![Python](https://img.shields.io/badge/python-3.12-blue) ![Relatórios](https://img.shields.io/badge/relatórios-LaTeX-green)

Trabalhos da disciplina **Métodos Quantitativos em Computação** (Ciência da Computação — Universidade de Fortaleza, 2026). A análise é feita em Python e os relatórios são escritos em LaTeX, com foco em dados reais de segurança pública do Ceará.

## Trabalhos

| Trabalho | Tema | Código | Relatório | Status |
|---|---|---|---|---|
| AV1 | Estatística descritiva dos CVLI no Ceará (2009–2025) | [`analise_cvli.py`](descritiva/analise_cvli.py) | [PDF](descritiva/relatorio_descritiva.pdf) | concluído |
| AV2 | Regressão linear | — | — | em andamento |
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

## Estrutura

```
metodos-quantitativos/
├── data/                  # base CVLI e documentação da fonte (SSPDS/CE)
├── descritiva/        # analise_cvli.py, relatorio_descritiva.pdf
├── figuras/
├── requirements.txt
└── README.md
```

Os demais trabalhos entram em pastas próprias (`av2-regressao/`, `av3-amostragem/`) conforme forem concluídos.

## Como executar

```bash
git clone https://github.com/GuilhermeMAzevedo/metodos-quantitativos.git
cd metodos-quantitativos

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS
pip install -r requirements.txt

cd descritiva
python analise_cvli.py
```

O script lê a base em `../data/`, abre os gráficos com `plt.show()` (feche cada janela para continuar) e salva os PDFs em `figuras/` e os CSVs de apoio em `saidas/` (ignorada pelo Git).

### Compilar o relatório

Use o Overleaf com o compilador **pdfLaTeX**, ou localmente:

```bash
cd descritiva
pdflatex relatorio_descritiva.tex
pdflatex relatorio_descritiva.tex     # segunda passada para o sumário
```

É preciso uma instalação completa do TeX Live (pacotes `babel` em português, `booktabs`, `multirow`, `makecell`, `listings`, `xurl`).

## Dados

A base é pública. Fonte, colunas e limitações em [`data/README.md`](data/README.md).

## Tecnologias

Python · pandas · matplotlib · LaTeX

## Autoria

Desenvolvido por [Guilherme Azevedo](https://github.com/GuilhermeMAzevedo).

