import ollama
from core.config import settings
from typing import Iterator

class LLMEngine:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.client = ollama.Client(host=base_url)

    def generate(
        self,
        prompt: str,
        model: str = None,
        system_prompt: str = "",
        options: dict = None
    ) -> str:
        """Geração de texto simples e direta com suporte a opções do modelo."""
        from core.model_manager import model_manager
        model = model or settings.DEFAULT_MODEL
        opts = options or model_manager.get_model_params(model)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(model=model, messages=messages, options=opts)
        return response['message']['content']
        
    def stream_chat(
        self,
        messages: list,
        model: str = None,
        options: dict = None,
        keep_alive: str = None
    ) -> Iterator[str]:
        """Geração de texto em streaming para a interface com suporte a parâmetros customizados."""
        from core.model_manager import model_manager
        model = model or settings.DEFAULT_MODEL
        opts = options or model_manager.get_model_params(model)

        stream = self.client.chat(
            model=model,
            messages=messages,
            stream=True,
            options=opts,
            keep_alive=keep_alive
        )
        for chunk in stream:
            content = chunk.get('message', {}).get('content', '')
            if content:
                yield content

    def get_available_models(self) -> list[str]:
        """Retorna uma lista de modelos baixados localmente no Ollama."""
        from core.model_manager import model_manager
        return model_manager.get_installed_tags()
