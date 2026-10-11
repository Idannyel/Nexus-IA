# Nexus IA

Bem-vindo ao **Nexus IA**! Este projeto é uma interface web moderna e 100% offline, projetada para rodar modelos de Inteligência Artificial usando o [Ollama](https://ollama.com/).

## Funcionalidades Principais

- **100% Local e Seguro**: Seus dados processados diretamente na sua máquina, garantindo total privacidade.
- **Design Elegante**: Interface moderna em "dark mode", inspirada em grandes soluções como ChatGPT e Claude.
- **Respostas em Tempo Real**: Streaming de texto instantâneo token a token.
- **Ferramentas Avançadas**: 
  - Renderização completa de *Markdown*.
  - Syntax Highlighting para blocos de código.
  - Botão de cópia rápida.
- **Controle de Criatividade**: Ajuste a temperatura (criatividade) do modelo diretamente pela interface (0.0 a 1.0).
- **Feedback Visual**: Tratamento de erros amigável caso o serviço Ollama não esteja rodando.

## Estrutura do Projeto

O código principal do projeto se encontra organizado em:

- `ui/` - Interface Streamlit moderna e estilizada (`app.py`, `styles.py`, `icons.py`).
- `core/` - Motor de orquestração e integração com Ollama (`llm_engine.py`, `orchestrator.py`, `config.py`).
- `memory/` - Pipeline RAG vetorial ChromaDB para indexação de documentos (`rag_pipeline.py`).
- `tools/` - Ferramentas de terminal seguras (`shell_tool.py`).
- `run.sh` e `run.bat` - Scripts para iniciar a aplicação.

## Pré-requisitos

Para rodar este projeto, você precisa de:
1. **[Ollama](https://ollama.com/)**: Instalado na máquina para processar os modelos de linguagem locais (ex.: `gemma3`, `llama3`).
2. **Python 3.10+**: Com ambiente virtual `.venv` configurado.

## Como iniciar

Execute o script de inicialização ou o Streamlit diretamente:

```bash
streamlit run ui/app.py
```

---

<p align="center">
  <i>Feito com dedicação para a comunidade de Inteligência Artificial Open Source.</i>
</p>
