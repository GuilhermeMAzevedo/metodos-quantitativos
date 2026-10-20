# Dados

```
data/
├── README.md
├── CVLI_2009-a-2025.xlsx          # SSPDS/CE (AV1 e AV2)
├── raw/                           # IBGE, arquivos brutos baixados, sem edição (AV2)
├── ibge_ce.csv                    # derivado: população e PIB per capita dos 184 municípios (AV2)
└── cvli_por_municipio.csv         # derivado: CVLI 2021-2023 por município (AV2)
```

## CVLI — `CVLI_2009-a-2025.xlsx`

Crimes Violentos Letais Intencionais (CVLI) no Ceará, de 2009 a 2025, com **um registro por vítima** (59.340 registros).

- **Fonte:** Secretaria da Segurança Pública e Defesa Social do Ceará (SSPDS/CE), Gerência de Estatística e Geoprocessamento (GEESP/SUPESP) — indicadores detalhados 2009–2025.
- **Link:** https://www.ce.gov.br/sspds/estatisticas/dados-detalhados/
- **Acessado em:** 07/09/2026
- **Aba usada:** `CVLI`

### O que é CVLI

Segundo a metodologia da SSPDS/CE, CVLI é a soma de homicídio doloso (incluindo feminicídio), lesão corporal seguida de morte e roubo seguido de morte (latrocínio). Mortes por intervenção policial não entram na contagem.

### Colunas

| Coluna | Descrição |
|---|---|
| `Município` | município da ocorrência (184 no total) |
| `AIS` | Área Integrada de Segurança (36 no total) |
| `Natureza` | tipo do crime |
| `Data` | data da ocorrência |
| `Hora` | horário da ocorrência (`HH:MM:SS`) |
| `Dia da Semana` | dia da semana |
| `Meio Empregado` | arma de fogo, arma branca, outros meios ou não informado |
| `Gênero` | gênero da vítima |
| `Idade da Vítima` | idade em anos; mistura números e o texto `Não Informada` |
| `Escolaridade da Vítima` | nível de escolaridade |
| `Raça da Vítima` | raça/cor |

### Limitações

- `Idade da Vítima` é `Não Informada` em 5.134 registros; as medidas de idade usam os 54.206 restantes.
- `Raça da Vítima` é `Não Informada` em 77,72% dos registros, e `Escolaridade da Vítima` em 28,44%.

---

## IBGE (AV2)

### Dados brutos (`raw/`)

Arquivos exatamente como foram baixados, sem edição.

| Arquivo | Conteúdo | Fonte | Acessado em |
|---|---|---|---|
| `ibge_populacao_censo2022.csv` | população residente por município, Censo 2022 (Ceará) | IBGE, SIDRA, tabela 4714 — *Censo Demográfico 2022: população residente, área territorial e densidade demográfica* | `20/10/2026` |
| `ibge_pib_municipios_2010_2023.xlsx` | PIB dos Municípios, 2010 a 2023, todo o Brasil (base de dados) | IBGE, *Produto Interno Bruto dos Municípios* | `20/10/2026` |

- População: https://sidra.ibge.gov.br/tabela/4714
- PIB dos Municípios: https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html

O PIB municipal mais recente publicado é o de 2023. O de 2024 foi adiado para 2027 (Nota Técnica 01/2026 do IBGE). O ano usado neste trabalho é **2022**, o mesmo do Censo.

### Como obter os dados

1. **População:** na tabela 4714 do SIDRA, escolher Município, filtrar o Ceará (184 municípios), variável *População residente* e ano 2022. No layout, deixar Variável e Ano no cabeçalho e Unidade Territorial nas linhas (uma linha por município, ao lado da população). Baixar em Excel (.xlsx).
2. **PIB:** na página do produto, baixar a base de dados do PIB dos Municípios (2010–2023, todo o Brasil). O filtro para Ceará e 2022 é feito pelo script.
3. Salvar os dois arquivos em `data/raw/` sem editar o conteúdo (o nome do arquivo de população deve conter `popul` e o do PIB, `pib`) e executar `python regressao/preparar_ibge.py`.

### `ibge_ce.csv` (derivado)

Gerado por `regressao/preparar_ibge.py` a partir de `raw/`: 184 linhas, uma por município do Ceará, com o PIB filtrado para o ano de 2022.

| Coluna | Descrição |
|---|---|
| `municipio` | nome do município, sem o sufixo de UF (" - CE") |
| `populacao` | população residente, Censo 2022 |
| `pib_per_capita` | PIB per capita municipal de 2022, a preços correntes (confirmar a unidade na planilha original) |

### `cvli_por_municipio.csv` (derivado)

Gerado por `regressao/analise_regressao.py` a partir de `CVLI_2009-a-2025.xlsx`: total de CVLI por município nos anos de **2021 a 2023**, três anos em torno do Censo 2022. Tem 184 linhas e soma 9.239 casos; 3 municípios têm zero casos no período e entram com `0`.

| Coluna | Descrição |
|---|---|
| `Município` | nome do município (mesmo texto da base original) |
| `cvli_2021_2023` | total de CVLI no período |

### Junção das bases

Os nomes são normalizados (sem acento, minúsculos, sem espaços nas pontas) antes da junção, porque a grafia difere entre SSPDS e IBGE. A junção deve casar os 184 municípios.

### Limitações

- O PIB per capita do IBGE usa uma base populacional própria, diferente da população do Censo usada aqui como variável explicativa.
- O CVLI cobre 2021–2023, enquanto população e PIB são de 2022.