# TrabalhoDas2
Trabalho disciplina Design e arquitetura de sistema

# 📊 VendaMais — Plataforma de Inteligência Operacional

> **Projeto Integrador** | Design e Arquitetura de Software II | UNIVILLE | 2026/1

## Sobre o Projeto

A **VendaMais Distribuidora Ltda.** é uma empresa de médio porte do setor de distribuição de bens de consumo, com operações em 4 estados, ~1.200 clientes ativos e ~3.500 pedidos processados por mês.

O problema central é a **ausência de visibilidade consolidada** sobre indicadores operacionais: relatórios levam até 2 dias para compilação manual, a inadimplência é calculada em planilhas desatualizadas e a diretoria toma decisões com dados de até 30 dias de defasagem.

### Solução

Uma **Plataforma de Inteligência Operacional** que automatiza a extração, transformação e visualização de dados do ERP, utilizando um pipeline de dados na nuvem Azure:

```
ERP → Azure Functions (Ingestão) → Blob Storage → Azure Functions (Transformação) → Azure SQL → Power BI
```

Ao final, a VendaMais poderá consultar seus KPIs com **defasagem máxima de 24 horas**, sem intervenção manual.

## 👥 Integrantes

<!-- Preencher com os dados da equipe -->

| Nome | GitHub |
|------|--------|
| Integrante 1 Alícia Souza| [@github](https://github.com/AliciaSchiochetSouza/) |
| Integrante 2 Felipe Dalçoquio| [@github](https://github.com/felipedalcoquio/) |
| Integrante 3 Lucas Zultanski| [@github](https://github.com/LucasZultanski/) |
| Integrante 4 Guilherme Miranda| [@github](https://github.com/guilhermesilvasanttos/) |


## 📁 Estrutura do Repositório

```
/
├── README.md                          # Este arquivo
├── docs/
│   ├── c4/
│   │   ├── 01-context.md             # C4 Nível 1 — Diagrama de Contexto
│   │   └── 02-container.md           # C4 Nível 2 — Diagrama de Container
│   └── adr/
│       ├── ADR-001.md                # Decisão: Estratégia de Ingestão (Serverless)
│       └── ADR-002.md                # Decisão: Estratégia de Armazenamento (Azure SQL)
```

## 📖 Navegação da Documentação

### Diagramas C4 (Arquitetura)

Os diagramas seguem o **C4 Model** e estão escritos em **Mermaid**, renderizando automaticamente no GitHub.

| Nível | Arquivo | Descrição |
|-------|---------|-----------|
| **N1 — Contexto** | [`docs/c4/01-context.md`](docs/c4/01-context.md) | Visão geral do sistema, usuários e sistemas externos |
| **N2 — Container** | [`docs/c4/02-container.md`](docs/c4/02-container.md) | Decomposição em 5 containers Azure com tecnologias e protocolos |

### ADRs (Decisões Arquiteturais)

Os ADRs documentam as decisões técnicas com contexto, alternativas consideradas (mín. 3) e trade-offs.

| ADR | Arquivo | Decisão |
|-----|---------|---------|
| **ADR-001** | [`docs/adr/ADR-001.md`](docs/adr/ADR-001.md) | Estratégia de Ingestão → Azure Functions (Serverless) |
| **ADR-002** | [`docs/adr/ADR-002.md`](docs/adr/ADR-002.md) | Estratégia de Armazenamento → Azure SQL Database |

## 🛠️ Tecnologias

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| Ingestão | Azure Functions (Python 3.11) | Extração diária de dados do ERP |
| Armazenamento | Azure Blob Storage | Repositório de dados brutos e processados |
| Transformação | Azure Functions (Python 3.11) | Limpeza e regras de negócio |
| Banco de Dados | Azure SQL Database | Tabelas analíticas (fonte de verdade) |
| Consumo | Power BI Service | Dashboards interativos por área |


> **Disciplina:** Design e Arquitetura de Software II — 7.º Semestre  
> **Professor:** Christiano Piccinin  
> **Instituição:** UNIVILLE — Joinville, SC — 2026

