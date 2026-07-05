# Pacote de Replicação: DesignRAG

Bem-vindo ao pacote de replicação anônimo do artigo submetido para revisão por pares: **"Improving the Quality of AI-Generated User Interfaces through Multimodal Retrieval of Proprietary Design System Artifacts"**.

⚠️ **Nota sobre Propriedade Intelectual:** O código-fonte do motor de inferência *backend* do DesignRAG e os microsserviços de integração no Figma desenvolvidos nesta pesquisa estão sujeitos a acordos de Propriedade Intelectual (PI) e sigilo industrial, não podendo ser disponibilizados publicamente. 
No entanto, em estrita conformidade com as diretrizes de Ciência Aberta para avaliações empíricas, este repositório disponibiliza **todos os dados brutos, o conjunto de referência (*ground truth*), as inferências completas de todos os modelos avaliados e os *scripts* estatísticos**, garantindo a total auditabilidade e reprodutibilidade da análise quantitativa do estudo.

---

## 📁 Estrutura do Repositório

O repositório está organizado logicamente para facilitar a auditoria do experimento passo a passo:

* `/dataset/`
  * `miniatures/`: Contém as 207 renderizações visuais em pixels (PNG) utilizadas na pesquisa.
  * `data_json_context.json`: Metadados extraídos (JSON), propriedades estruturais e o contexto semântico gerado pelos LLMs multimodais.
* `/queries/`
  * `queries.json`: Conjunto de dados contendo as 30 intenções de busca estratificadas (em Inglês e Português) e o mapeamento do gabarito oficial validado.
* `/demo/`
  * Demonstração em vídeo anonimizada da execução do pipeline em tempo real.
* `/stats/`
  * `Analysis_P@K_MRR/` *(Análise Descritiva)*
    * `metrics.json`: Resultados brutos de performance (P@k e MRR) de todas as consultas em todos os modelos.
    * `Analysis.py`: Script para extração das médias de recuperação por modelo.
    * `results_metrics.txt`: **[Output] Tabela consolidada com as médias (P@1, P@3, P@5, MRR)**.
  * `Fleiss_Kappa/` *(Validação do Conjunto de Referência)*
    * `team_responses.csv`: Anotações brutas do painel de especialistas (seleções individuais).
    * `Fleiss_Kappa.py`: Script para cálculo do nível de concordância entre os avaliadores.
    * `result_Fleiss_Kappa.txt`: **[Output] Score de concordância Fleiss' Kappa**.
    * `consolidated_ground_truth.py`: Script que processa a votação majoritária e gera o gabarito.
    * `result_consolidated_ground_truth.csv`: **[Output] Gabarito oficial utilizado no experimento**.
  * `Friedman_Wilcoxon/` *(Estatística Inferencial)*
    * `mrr_results.json`: Vetores de resultados de MRR isolados para as 30 consultas.
    * `Friedman_Wilcoxon.py`: Script para cálculo do Teste Global (Friedman) e comparações pareadas (Wilcoxon *signed-rank* com correção Holm-Bonferroni).
    * `result_Friedman_Wilcoxon.txt`: **[Output] Resultados da significância estatística**.
  
---

## 📊 Resumo dos Resultados Estatísticos

A eficácia da arquitetura DesignRAG foi validada por meio de testes não paramétricos aplicados às pontuações de recuperação (MRR). Os resultados detalhados (disponíveis na pasta `/stats`) atestam que:

1. **Concordância dos Especialistas:** A validação do *Ground Truth* obteve um score Fleiss' Kappa de **0.2630** (Concordância Moderada), estabelecendo uma base sólida para avaliar a ambiguidade natural de componentes de UI.
2. **Diferença Global:** O Teste de Friedman confirmou uma variação global altamente significativa no desempenho dos modelos avaliados (**$p < 0.0001$**).
3. **Superioridade Multimodal:** Os testes pareados de Wilcoxon comprovaram que todas as variantes multimodais (DesignRAG) superaram estatisticamente ambas as linhas de base unimodais (FTS e RAG Puramente Textual), com **$p_{adj} < 0.05$**.

---

## 🎥 Demonstração de Execução (Vídeo)

Para ilustrar o pipeline e o tempo de resposta em um cenário de uso realista, gravamos uma demonstração visual do motor de inferência. O vídeo demonstra:
1. A seleção da intenção de busca em linguagem natural.
2. A inferência paralela comparando as linhas de base unimodais com os LLMs multimodais.
3. A renderização do Top-5 em colunas pareadas, destacando a checagem de conformidade visual (Verde/Vermelho) contra o *Ground Truth*.

<video src="demo/designrag.mp4" controls="controls" style="max-width: 100%;">
  Seu navegador não suporta a tag de vídeo. <a href="demo/designrag.mp4">Clique aqui para baixar o vídeo</a>.
</video>

---

## 🚀 Como Reproduzir a Análise Estatística

Os avaliadores podem auditar a matemática e os valores de p-value reportados no artigo executando os scripts Python fornecidos. 

**Passo a passo para execução:**
1. Clique no botão de **Download (ZIP)** no canto superior direito desta página para baixar o pacote de replicação completo.
2. Descompacte o arquivo em sua máquina local e abra o terminal na pasta extraída.

**Pré-requisitos:**
* Python 3.10+
* Bibliotecas: `numpy`, `packaging`, `pandas`, `patsy`, `python-dateutil`, `scipy`, `six`, `statsmodels`

**Execução no Terminal:**
```bash
# Instale as dependências de análise
pip install -r stats/requirements.txt

# 1. Consolidar o ground truth e validar o comitê de especialistas:
python stats/Fleiss_Kappa/consolidated_ground_truth.py
python stats/Fleiss_Kappa/Fleiss_Kappa.py

# 2. Calcular as médias métricas descritivas (Precision e MRR):
python stats/Analysis_P@K_MRR/Analysis.py

# 3. Auditar a significância estatística (Friedman e Wilcoxon):
python stats/Friedman_Wilcoxon/Friedman_Wilcoxon.py
```

