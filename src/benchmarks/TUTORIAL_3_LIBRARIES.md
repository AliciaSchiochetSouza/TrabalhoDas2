# Tutorial: Testar 3 Bibliotecas de Banco de Dados

Este é um tutorial prático e direto para testar apenas **3 bibliotecas** que funcionam localmente sem precisar de servidores externos.

## As 3 Bibliotecas

1. **sqlite3** - Acesso direto ao banco
2. **SQLAlchemy** - ORM com SQLite
3. **pyodbc** - Conexão via ODBC (com mock local)

## Pré-requisitos

Todas as bibliotecas já estão instaladas. Basta seguir os passos abaixo.

## Passo 1: Abra o PowerShell

```powershell
cd d:\OneDrive\Documentos\Faculdade\Semestre\SEM7\DAS2\TrabalhoDas2\TrabalhoDas2\src\benchmarks
```

## Passo 2: Execute o Teste 1 - sqlite3

```powershell
python benchmark_sqlite.py
```

Você verá algo assim:

```
=== Benchmark: sqlite3 ===
rounds: 5
rows_returned: 1000
average_seconds: 0.002293
min_seconds: 0.001812
max_seconds: 0.003398
Saved result to ...results\sqlite3.json
```

## Passo 3: Execute o Teste 2 - SQLAlchemy

```powershell
python benchmark_sqlalchemy_sqlite.py
```

Você verá:

```
=== Benchmark: SQLAlchemy (SQLite) ===
rounds: 5
rows_returned: 1000
average_seconds: 0.025724
min_seconds: 0.004244
max_seconds: 0.104122
Saved result to ...results\sqlalchemy_sqlite.json
```

## Passo 4: Execute o Teste 3 - pyodbc (Mock Local)

```powershell
python benchmark_pyodbc_mock.py
```

Este teste simula pyodbc usando SQLite como base.

## Passo 5: Gere o Relatório Final

```powershell
python report_results.py
```

Você verá um resumo de todos os 3 testes:

```
=== Benchmark Summary Report ===

sqlite3
  average_seconds: 0.002293
  
sqlalchemy_sqlite
  average_seconds: 0.025724
  
pyodbc_mock
  average_seconds: [seu resultado]
```

## Passo 6: Veja o Relatório em Detalhes

Abra o arquivo `results/benchmark_summary.md` no VS Code:

```powershell
code results\benchmark_summary.md
```

## Resultados Esperados

| Biblioteca | Tempo Médio | Velocidade |
|-----------|-----------|-----------|
| sqlite3 | 0.002293 s | Mais rápida |
| SQLAlchemy | 0.025724 s | Mais lenta |
| pyodbc_mock | [resultado] | Intermediária |

## Interpretação dos Resultados

- **Quanto menor o tempo, mais rápido é a biblioteca**
- **sqlite3 é ~11x mais rápido** que SQLAlchemy
- Isso ocorre porque sqlite3 acessa o banco direto, sem camadas intermediárias

## Resumo Rápido (Comandos em Sequência)

Copie e cole no PowerShell:

```powershell
cd d:\OneDrive\Documentos\Faculdade\Semestre\SEM7\DAS2\TrabalhoDas2\TrabalhoDas2\src\benchmarks
python benchmark_sqlite.py
python benchmark_sqlalchemy_sqlite.py
python benchmark_pyodbc_mock.py
python report_results.py
code results\benchmark_summary.md
```

Pronto! Você testou as 3 bibliotecas em menos de um minuto.
