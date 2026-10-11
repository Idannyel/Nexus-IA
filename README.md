# Nexus IA

Bem-vindo ao **Nexus IA**! Uma plataforma corporativa autônoma de inteligência artificial executada **100% offline e localmente**, utilizando o [Ollama](https://ollama.com/) como motor de inferência.

O Nexus IA conta agora com integração nativa às famílias de modelos especializados **DeepSeek** (raciocínio lógico, matemática e código) e **Dolphin** (conversação, redação e criatividade sem filtros), além de um seletor dinâmico e central de gerenciamento de hardware.

---

## Funcionalidades Principais

- **Execução 100% Local e Privada**: Processamento direto na máquina, sem envio de conversas, arquivos ou embeddings para servidores externos ou APIs pagas.
- **Modelos Especializados Integrados**:
  - **DeepSeek** (`deepseek-r1:1.5b`, `deepseek-coder:1.3b`, `deepseek-r1:7b`, `deepseek-r1:8b`): Especialista em raciocínio analítico, resolução de problemas passo a passo (CoT), matemática e engenharia de software. Suporte a blocos de reflexão analítica (`<think>`).
  - **Dolphin** (`dolphin-phi:2.7b`, `dolphin-mistral:7b`, `dolphin-llama3:8b`): Especialista em conversação fluida, escrita criativa, síntese e ideação sem barreiras artificiais.
- **Central de Modelos e Diagnóstico de Hardware**:
  - Medição em tempo real de RAM disponível, espaço livre em disco e aceleração de hardware.
  - Avaliador preditivo de compatibilidade para evitar sobrecarga ou travamento por falta de memória/disco.
  - Download via streaming com barra de progresso em tempo real e cálculo de MB transferidos.
  - Descarregamento sob demanda de modelos da memória RAM (`keep_alive=0`).
  - Ajuste de parâmetros de inferência por modelo (temperatura, limite de tokens, top-p) com persistência e restauração.
- **Memória Vetorial & RAG**: Indexação local de documentos (PDF, TXT, MD, DOCX) com busca semântica integrada e preservação de contexto ao alternar modelos.
- **Ferramentas de Terminal Seguras**: Execução de comandos no shell (`/shell <comando>`) com validação de segurança.
- **Design Moderno em Dark Mode**: Estilo minimalista inspirado em ChatGPT e Gemini, sem dependências externas de CSS.

---

## Estrutura do Projeto

- `core/`
  - `model_manager.py`: Inspeção de hardware, catálogo estruturado de variantes, integração com API do Ollama e persistência de parâmetros.
  - `orchestrator.py`: Orquestração do agente, injeção de diretrizes específicas por família de modelo e gerenciamento de ferramentas.
  - `llm_engine.py`: Motor de comunicação com o Ollama, controle de streaming e opções de inferência.
  - `config.py`: Configurações centrais e constantes de modelos padrão.
- `memory/`
  - `rag_pipeline.py`: Pipeline RAG vetorial com ChromaDB e embeddings locais.
- `tools/`
  - `shell_tool.py`: Execução segura de comandos de terminal.
- `ui/`
  - `app.py`: Interface Streamlit integrada com chat, central de modelos, arquivos e configurações.
  - `styles.py`: Sistema de design CSS completo (dark mode, cartões de hardware, think blocks).
  - `icons.py`: Biblioteca de ícones SVG vetoriais leves (sem emojis).

---

## Como Instalar e Rodar

### 1. Pré-requisitos
1. **Ollama**: Baixe e instale o [Ollama](https://ollama.com/).
2. **Python 3.10+** com ambiente virtual criado.

### 2. Baixar Modelos Recomendados no Ollama
Para computadores com restrição de RAM/disco ou uso em CPU, as seguintes variantes compactas são recomendadas:

```bash
# DeepSeek (Raciocínio - 1.1 GB em disco / ~2.5 GB RAM)
ollama pull deepseek-r1:1.5b

# Dolphin (Conversação - 1.6 GB em disco / ~3.5 GB RAM)
ollama pull dolphin-phi:2.7b
```

Caso disponha de 8 GB+ de RAM livre e mais espaço em disco:
```bash
ollama pull deepseek-r1:7b
ollama pull dolphin-mistral:7b
```

### 3. Iniciar a Aplicação

No Windows:
```bash
.\run.bat
```

Ou diretamente pelo Streamlit:
```bash
streamlit run ui/app.py
```

### 4. Executar Testes Automatizados
```bash
python test_nexus.py
python test_model_manager.py
```
