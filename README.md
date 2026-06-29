# Prime D'Or | RH Analytics Dashboard

> Dashboard estratégico de Gente & Gestão para HRBP — 100% offline, sem dependências de API.

![Dashboard Preview](https://img.shields.io/badge/Status-Producao-brightgreen) ![ES5](https://img.shields.io/badge/JS-ES5%20Compatible-blue) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Sobre o Projeto

Dashboard analítico completo de RH desenvolvido para a posição de **HRBP Senior — Unidade Hospitalar RJ** da **Prime D'Or (Rede D'Or São Luiz)**. Combina dados reais do ESG 2023, benchmarks ANAHP e pesquisa salarial (Robert Half + MR Survey 2024) com projeções modeladas para fins de demonstração de domínio em **People Analytics**.

**Propósito:** Demonstrar capacidade analítica, domínio de indicadores de RH e construção de dashboards executivos sem dependência de licença Power BI Premium.

---

## Funcionalidades

| Modulo | Descricao |
|---|---|
| **Capa Executiva** | KPI strip, alertas de status, descricao dos modulos, graficos resumo |
| **Turnover & Movimentacao** | Mensal, por cargo, admissoes vs desligamentos, motivos de saida |
| **Cargos & Salarios** | Pesquisa de mercado: gap vs P50/P75, custo total por cargo, tabela comparativa |
| **Desempenho & Clima** | Matriz 9-Box, radar de clima, eNPS trimestral, T&D por area |
| **Orcamento OPEX/CAPEX** | Budget vs realizado, alertas de desvio, projetos de investimento |
| **Benchmarks** | Turnover, eNPS, absenteismo e T&D vs 7 players do setor hospitalar |
| **Analise Preditiva** | 4 cenarios com planos de acao + simulador de impacto financeiro |
| **Plano de Acao** | Kanban 30/90/180 dias, framework 5W2H, Matriz RACI |
| **Assistente IA Offline** | Base de conhecimento local — responde sobre qualquer KPI sem API |
| **Relatorio Diretoria** | PDF de 2 paginas gerado diretamente no browser (Ctrl+P) |
| **Tema Dark/Light** | Toggle instantaneo com persistencia dos graficos |

---

## Estrutura de Arquivos

```
prime-dor-rh-dashboard/
├── index.html              # Dashboard completo (single-file, 100% offline)
├── data.json               # Base de dados estruturada (18 cargos, 12 meses, benchmarks)
├── base_rh_prime_dor.xlsx  # Planilha Excel com 8 abas e 144 formulas (fonte dos dados)
└── README.md
```

---

## Como Usar

### Localmente
```bash
# Clone o repositorio
git clone https://github.com/SEU_USUARIO/prime-dor-rh-dashboard.git

# Abra o arquivo no browser (sem servidor necessario)
open index.html
# ou simplesmente arraste o arquivo para o Chrome/Edge/Firefox
```

### GitHub Pages (deploy gratuito)
1. Fork ou clone este repositorio
2. Va em **Settings > Pages**
3. Selecione **Branch: main** e pasta **/ (root)**
4. O dashboard estara disponivel em `https://SEU_USUARIO.github.io/prime-dor-rh-dashboard`

---

## Stack Tecnica

- **HTML/CSS/JS** — ES5 puro (compativel com qualquer browser, incluindo WebViews Android antigas)
- **Chart.js 3.9.1** — graficos interativos (UMD, sem bundler)
- **chartjs-plugin-datalabels 2.0.0** — labels nos graficos
- **Zero backend** — todos os dados embutidos no HTML via JSON
- **Zero dependencias de build** — abre direto no browser

---

## Dados & Metodologia

| Fonte | Uso |
|---|---|
| Rede D'Or ESG / Relatorio de Sustentabilidade 2023 | Headcount, composicao, programas de RH |
| ANAHP Observatorio 2023/2024 | Benchmarks setoriais (turnover, absenteismo) |
| Robert Half Guia Salarial 2024 | Pesquisa salarial P50/P75 |
| Michael Robert Survey 2024 | Validacao salarial cross-reference |
| Glassdoor / Indeed | eNPS estimado e percepcao publica |

> **Nota:** Dados mensais por unidade sao **projecoes modeladas** a partir das fontes acima. Em producao, substitua pelos dados reais do HRIS.

### Indicadores Cobertos
- Turnover (total, voluntario, por cargo)
- Absenteismo mensal
- eNPS e pesquisa de clima por pilar
- Matriz 9-Box
- Orcamento OPEX/CAPEX vs realizado
- Pesquisa salarial (gap vs P50/P75)
- Benchmarks vs 7 players (Sirio-Libanes, Hapvida, Fleury, Dasa, Mater Dei, ANAHP)
- Analise preditiva em 4 cenarios

---

## Customizacao

Para adaptar ao seu contexto real:

1. **Substitua os dados** no bloco `var D={...}` do `index.html` pelos seus dados reais
2. **Ou use** a planilha `base_rh_prime_dor.xlsx` como modelo e exporte para JSON
3. **Altere a marca** buscando `Prime D'Or` no HTML e substituindo pelo nome da sua organizacao

---

## Autor

**J. Gustavo Loureiro Campos Silva**
Analista de Dados e Processos | HRBP Analytics

[![LinkedIn](https://img.shields.io/badge/LinkedIn-josegustavoloureiro-blue)](https://linkedin.com/in/josegustavoloureiro)
[![GitHub](https://img.shields.io/badge/GitHub-jgustavoloureiro-black)](https://github.com/jgustavoloureiro)

---

## Licenca

MIT — livre para uso, adaptacao e distribuicao com atribuicao.
