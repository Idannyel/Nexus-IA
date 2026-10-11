from core.llm_engine import LLMEngine
from core.config import settings
from memory.rag_pipeline import RAGPipeline
from tools.shell_tool import ShellTool

class AgentOrchestrator:
    def __init__(self):
        self.llm = LLMEngine()
        self.rag = RAGPipeline()
        self.shell = ShellTool()

    def process_message(self, user_message: str, history: list, persona: str, use_rag: bool = False, use_tools: bool = False):
        """Processa a mensagem do usuário, injeta contexto (RAG) e gerencia ferramentas."""
        
        system_prompt = settings.PERSONAS.get(persona, settings.PERSONAS["Assistente Rápido"])
        
        # 1. Recuperar contexto do RAG (se ativado)
        context = ""
        if use_rag:
            rag_context = self.rag.query_documents(user_message)
            if rag_context:
                context += f"\n\nContexto dos documentos locais:\n{rag_context}\n"
        
        # 2. Executar ferramentas básicas (se ativado) - Simplificação de Tool Calling
        # Para uma implementação de tool calling real local, usaria-se parsing do output do LLM.
        # Aqui injetamos comandos explicitamente detectados para fins de demonstração.
        if use_tools:
            if user_message.lower().startswith("/shell"):
                cmd = user_message[6:].strip()
                result = self.shell.execute(cmd)
                context += f"\n\nResultado da execução do comando '{cmd}':\n{result}\n"

        # 3. Construir o Prompt final
        if context:
            system_prompt += f"\n\nInformações adicionais para basear sua resposta:{context}"

        system_prompt += settings.LANGUAGE_RULE

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # 4. Retornar stream
        return self.llm.stream_chat(messages=messages)
