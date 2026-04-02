# 📊 Terminal Financeiro - Power BI

Dashboard interativo desenvolvido no Power BI para análise de ativos da bolsa brasileira, com foco em **risco, retorno e contexto macroeconômico**.

---

## 🚀 Objetivo

O projeto foi criado para ir além de visualizações estáticas, oferecendo uma ferramenta que permita:

- Comparar ativos de forma dinâmica  
- Avaliar risco vs retorno  
- Analisar desempenho por setor  
- Acompanhar indicadores macroeconômicos  

---

## 📸 Preview

<div align="center">
      <img width="1481" height="833" alt="Image" src="https://github.com/user-attachments/assets/d4a19c08-b1a1-4ee1-92ee-810cb07e6032" />
</div>
<br>

<div align="center">
  <table>
    <tr>
      <td width="50%">
        <img width="1481" height="834" alt="Image" src="https://github.com/user-attachments/assets/42c7555b-bec8-4ce5-88e9-e772e9c6d6b8" width="100%" />
      </td>
      <td width="50%">
        <img width="1485" height="836" alt="Image" src="https://github.com/user-attachments/assets/eaa768db-dc3b-4653-ad84-325c0e2cb1e3"  width="100%"/>
      </td>
    </tr>
  </table>
</div>

📹 Vídeo demonstrativo do dashboard disponível no LinkedIn:  
[Assistir à demonstração](https://www.linkedin.com/posts/gabrielsantos1509_powerbi-dataanalytics-businessintelligence-activity-7445455083095441409-xRKK?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEkTkOkBSaoGpEzpEivH-Rj7Tibcm-sPEIg)

---

## 🧠 Principais Funcionalidades

- 📈 Comparação de ativos (ações e fundos)
- ⚖️ Análise de risco vs retorno (volatilidade x rentabilidade)
- 🏢 Visualização por setor e indústria
- 💰 Indicadores macro: Selic, IPCA e dólar
- 🔄 Atualização automática dos dados
- 🎛️ Filtros e parâmetros dinâmicos

---

## 🏗️ Arquitetura de Dados

O modelo foi estruturado seguindo boas práticas de BI:

- **Star Schema**
  - Tabelas fato: preços históricos, dividendos  
  - Tabelas dimensão: ativos, categorias, calendário  

- Uso de **DAX avançado** para:
  - Controle de contexto  
  - Cálculos de rentabilidade  
  - Comparação com benchmarks  

---

## ⚙️ Pipeline de Dados (ETL)

A coleta e tratamento dos dados foram automatizados com Python:

- Extração via `yfinance`
- Tratamento de:
  - Preços históricos  
  - Dividendos  
  - Indicadores macroeconômicos  
- Geração de arquivos `.csv` consumidos pelo Power BI  

---

## 🔄 Automação

- Workflow automatizado com **Git + GitHub**
- Atualização dos dados **de segunda a sexta às 19h**
- Simulação de fluxo real (D-1)

---

## 🎨 Customizações

Para melhorar a experiência do usuário:

- Uso de **HTML/CSS dentro do Power BI**  
- Criação de elementos visuais personalizados (SVG)  
- Parâmetros dinâmicos para interação entre gráficos  

---

## 🧩 Principais Desafios

- Tratamento correto de **dividendos**
- Ajuste de **desdobramentos (splits)**
- Evitar distorções em análises de longo prazo
- Garantir consistência entre ativos e benchmarks  

---

## 🛠️ Tecnologias Utilizadas

- Power BI  
- DAX  
- Python  
- yfinance  
- Git & GitHub  

---

## 🚀 Próximos Passos

- Implementar novas métricas financeiras (ex: P/VP, Sharpe)  
- Melhorar análise de retorno real  
- Refinar comparações entre ativos  
- Evoluir a camada visual (UX/UI)  

---

## 📬 Contato

- LinkedIn: www.linkedin.com/in/gabrielsantos1509
- Portfólio: https://gabrielsantos-portfolio.vercel.app

---

## ⭐ Considerações

Este projeto foi desenvolvido como parte do meu portfólio, com foco em simular um cenário real de análise de dados no mercado financeiro.
