# Exoplanet Hunter

Análise exploratória dos objetos KOI (Kepler Objects of Interest) do NASA Exoplanet Archive.

## Dados de entrada

- Arquivo congelado: [data/cumulative.csv](data/cumulative.csv)
- Origem: [NASA Exoplanet Archive — tabela `cumulative`](https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+cumulative&format=csv)
- Consulta TAP: `select * from cumulative`
- Data da extração: 30/09/2026
- Verificação com a análise em `notebooks/01_eda.ipynb`: 9.564 registros, 153 colunas; classes `FALSE POSITIVE` = 4.839, `CANDIDATE` = 1.977 e `CONFIRMED` = 2.748.
- SHA-256: `A85348F20082D24FB14D4A05A9A44C644B801998FAD7CEC36F8980EB1F0A69AB`

O notebook carrega a cópia local para manter os resultados reprodutíveis. A tabela remota pode mudar; para reproduzir a análise desta entrega, use o CSV versionado.

## Ambiente

O projeto usa Python 3.11.9 e um ambiente virtual local `.venv`. No VS Code, abra a paleta de comandos, escolha **Python: Select Interpreter** e selecione `.venv\Scripts\python.exe` (Windows). Para os notebooks, selecione o kernel **Python (.venv) exoplanet-hunter**.

Criação/instalação do ambiente:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

As versões das bibliotecas usadas nesta entrega estão fixadas em [requirements.txt](requirements.txt).

## Entrega 2 — pré-processamento

O notebook [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)
compara 24 combinações de imputação, escala e redução com kNN fixo (`k=7`,
distância euclidiana, pesos uniformes). Utiliza o mesmo snapshot e as 12
grandezas da Entrega 1. As cinco divisões de `StratifiedGroupKFold` usam
`kepid` como grupo e semente 42; todas as transformações são ajustadas
somente no treino de cada fold. A menção a 10 folds na EDA não altera o
protocolo de cinco folds exigido nesta entrega.

Depois de instalar as dependências acima, selecione o kernel `.venv` e
execute todas as células na ordem. O notebook funciona a partir da raiz
do repositório ou de `notebooks/`; não baixa outra versão dos dados.
As funções de construção e execução ficam em `src/pipelines.py` e
`src/experiments.py`, enquanto a explicação acadêmica permanece no notebook.

Os resultados são salvos em `results/`:

- `preprocessing_folds.csv`: 120 registros, métricas, dimensões, tempo,
  estado, avisos e erros por combinação/fold.
- `preprocessing_summary.csv`: 24 combinações; médias e desvios amostrais
  somente para execuções com cinco folds válidos.
- `preprocessing_fold_scheme.csv` e `preprocessing_fold_assignments.csv`:
  diagnóstico de classes/grupos e associação exata dos objetos ao teste.
- `preprocessing_baseline_comparison.csv`: diferenças e empates em relação
  ao baseline para todas as métricas.
- `preprocessing_paired_effects.csv`: efeitos com as demais opções e folds
  mantidos iguais.
- `preprocessing_metadata.json`: versões efetivas, hashes e parâmetros.

O baseline usa mediana, sem escala e sem redução. Diferenças menores que o
maior desvio entre duas configurações são interpretadas como empate
descritivo, sem teste formal de significância. Tempos incluem ajuste,
previsões, métricas e registro das dimensões, com uma thread numérica.
Uma nova execução substitui somente os arquivos de resultados desta entrega;
a EDA e o CSV congelado são preservados.
