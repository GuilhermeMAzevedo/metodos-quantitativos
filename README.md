# Métodos Quantitativos em Computação

Trabalhos da disciplina **Métodos Quantitativos em Computação** (Ciência da Computação — Universidade de Fortaleza, 2026). A análise é feita em Python e os relatórios são escritos em LaTeX, com foco em dados reais de segurança pública do Ceará.

## Trabalhos

| Trabalho | Tema | Pasta | Status |
|---|---|---|---|
| AV1 | Estatística descritiva dos CVLI no Ceará (2009–2025) | `descritiva/` | em andamento |
| AV2 | Regressão linear | `regressao/` | planejado |
| AV3 | Estimação e amostragem | `amostragem/` | planejado |

## Dados

A base principal é a de **Crimes Violentos Letais Intencionais (CVLI)** da SSPDS/CE, com um registro por vítima. Fonte, colunas e limitações em [`data/README.md`](data/README.md).

## Estrutura prevista

```
metodos-quantitativos/
├── data/              # bases de dados e documentação das fontes
├── descritiva/    # script de análise + relatório LaTeX
├── regressao/
└── amostragem/
```

## Preparar o ambiente

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS
pip install -r requirements.txt
```

## Tecnologias

Python · pandas · matplotlib · LaTeX
