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
