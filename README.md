# Agente Autônomo de Pesquisa de Startups (Orquestrador Customizado)

Um sistema de múltiplos agentes totalmente autônomo, construído do zero em Python, para pesquisar startups e gerar relatórios estruturados e validados em formato JSON. Ele implementa o padrão ReAct (Reasoning + Acting), inspirado na arquitetura `autoresearch` de Andrej Karpathy, iterando autonomamente até que o relatório atinja a nota perfeita (100/100).

## Arquitetura

Este sistema elimina a dependência de CLIs de agentes de terceiros, utilizando um orquestrador Python customizado (`agent.py`) que gerencia a interação entre o LLM e ferramentas locais determinísticas:

1. **`agent.py` (O Cérebro)**: Um script Python que gerencia o histórico da conversa, chama o modelo Llama 3.3 via OpenRouter para raciocínio (*Thought*/*Action*), e executa comandos locais utilizando `subprocess`.
2. **`program.md` (Diretrizes Principais)**: Define o protocolo ReAct, instruindo o agente sobre os formatos de ferramentas (`RUN_SEARCH|query`, `WRITE_REPORT|json`, `RUN_EVALUATOR`) e as regras do loop.
3. **`research_tools.py` (Ferramenta de Busca)**: Ferramenta CLI desenvolvida com a biblioteca `ddgs` (DuckDuckGo) para fornecer dados web limpos.
4. **`evaluate.py` (O Juiz)**: Um auditor baseado em LLM que pontua o `report.json` com base em critérios estritos de Venture Capital e fornece feedback prescritivo para correções.

## Como Executar

1. Clone este repositório.
2. Certifique-se de estar usando o Python 3.12 (gerenciado via `pyenv`).
3. Ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure o `.env` com suas credenciais do OpenRouter:
   ```env
   OPENROUTER_API_KEY=sua_chave_aqui
   OPENROUTER_BASE_URL=[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)
   ```
6. Execute o agente passando a startup alvo:
   ```bash
   python agent.py "Mistral AI"
   ```

## Bônus: Melhoria de Pipeline para CRM

**A Melhoria:**
Este orquestrador customizado (`agent.py`) foi desenhado como um componente modular de **Engenharia de Dados**. Ele pode ser containerizado e implantado como um *worker* gerenciado por ferramentas como Apache Airflow. Acionado por um feed RSS de notícias, o loop garante a alta qualidade dos dados (via `evaluate.py`). Em vez de gerar um JSON local, a ação `WRITE_REPORT` pode ser adaptada para realizar um *upsert* direto em um banco relacional (ex: PostgreSQL ou DuckDB).

**A Ideia de Produto:**
Esse pipeline cria uma base proprietária, atualizada automaticamente e livre de alucinações. Essa fundação de dados é o *backend* ideal para alimentar o **CRM AI-native para profissionais de investimento**, permitindo que analistas consultem perfis robustos usando linguagem natural.