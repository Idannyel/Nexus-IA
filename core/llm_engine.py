import ollama
from core.config import settings
from typing import Iterator

class LLMEngine:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.client = ollama.Client(host=base_url)

    def generate(self, prompt: str, model: str = settings.DEFAULT_MODEL, system_prompt: str = "") -> str:
        """Geração de texto simples e direta."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(model=model, messages=messages)
        return response['message']['content']
        
    def stream_chat(self, messages: list, model: str = None) -> Iterator[str]:
        """Geração de texto em streaming para a interface."""
        model = model or settings.DEFAULT_MODEL
        stream = self.client.chat(model=model, messages=messages, stream=True)
        for chunk in stream:
            content = chunk['message']['content']
            if content:
                yield content

    def get_available_models(self) -> list[str]:
        """Retorna uma lista de modelos baixados localmente no Ollama."""
        try:
            models_info = self.client.list()
            return [m.get('name') or m.get('model') for m in models_info['models']]
        except Exception as e:
            print(f"Erro ao obter modelos: {e}")
            return []
