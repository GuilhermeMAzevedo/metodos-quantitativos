# Dados

## CVLI_2009-a-2025.xlsx

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
