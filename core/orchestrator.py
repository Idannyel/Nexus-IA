from core.llm_engine import LLMEngine
from core.config import settings
from memory.rag_pipeline import RAGPipeline
from tools.shell_tool import ShellTool

class AgentOrchestrator:
    def __init__(self):
        self.llm = LLMEngine()
        self.rag = RAGPipeline()
        self.shell = ShellTool()

    def build_system_prompt(
        self,
        persona: str = "Assistente Rápido",
        model_name: str = None,
        context: str = ""
    ) -> str:
        """Constrói as diretrizes de sistema incorporando persona, contexto e especializações de DeepSeek/Dolphin."""
        from core.model_manager import model_manager

        target_model = model_name or settings.DEFAULT_MODEL
        family = model_manager.detect_family(target_model)

        system_prompt = settings.PERSONAS.get(persona, settings.PERSONAS["Assistente Rápido"])

        if family == "deepseek":
            system_prompt += (
                "\n\n[DIRETRIZ DE RACIOCINIO - DEEPSEEK]: Pense metodicamente. "
                "Para problemas técnicos, matemática e programação, estruture a solução passo a passo, "
                "use blocos de código com sintaxe destacada e seja analiticamente rigoroso."
            )
        elif family == "dolphin":
            system_prompt += (
                "\n\n[DIRETRIZ DE CONVERSACAO - DOLPHIN]: Seja fluido, criativo e abrangente. "
                "Explore alternativas, forneça respostas completas e mantenha tom colaborativo sem bloqueios artificiais."
            )

        if context:
            system_prompt += f"\n\nInformações adicionais para basear sua resposta:{context}"

        system_prompt += settings.LANGUAGE_RULE
        return system_prompt

    def process_message(
        self,
        user_message: str,
        history: list,
        persona: str,
        use_rag: bool = False,
        use_tools: bool = False,
        model: str = None,
        options: dict = None
    ):
        """Processa a mensagem do usuário, injeta contexto (RAG), adapta prompt por família e gerencia ferramentas."""
        target_model = model or settings.DEFAULT_MODEL

        # 1. Recuperar contexto do RAG (se ativado)
        context = ""
        if use_rag:
            rag_context = self.rag.query_documents(user_message)
            if rag_context:
                context += f"\n\nContexto dos documentos locais (RAG):\n{rag_context}\n"

        # 2. Executar ferramentas básicas (se ativado)
        if use_tools:
            if user_message.lower().startswith("/shell"):
                cmd = user_message[6:].strip()
                result = self.shell.execute(cmd)
                context += f"\n\nResultado da execução do comando '{cmd}':\n{result}\n"

        # 3. Construir o Prompt final
        system_prompt = self.build_system_prompt(persona=persona, model_name=target_model, context=context)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # 4. Retornar stream com modelo e opções selecionadas
        return self.llm.stream_chat(messages=messages, model=target_model, options=options)
