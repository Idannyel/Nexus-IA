import os
from pydantic import BaseModel
from typing import List, Dict

class Settings(BaseModel):
    # Model Configurations
    DEFAULT_MODEL: str = "llama3.2:latest" # Replace with 'mistral', 'qwen', 'deepseek-coder' etc.
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Provider
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Vector DB
    VECTOR_DB_DIR: str = os.path.join(os.getcwd(), "data", "vector_db")
    
    # Personas
    PERSONAS: Dict[str, str] = {
        "Assistente Rápido": "Você é um assistente prestativo, claro e objetivo. Responda de forma concisa.",
        "Desenvolvedor": "Você é um Engenheiro de Software Sênior. Forneça respostas técnicas detalhadas, código limpo e siga as melhores práticas.",
        "Pesquisador": "Você é um analista investigativo. Forneça análises detalhadas, cite fontes de dados quando aplicável e seja rigoroso com as informações."
    }

    # Regra de idioma aplicada a todas as personalidades
    LANGUAGE_RULE: str = (
        "\n\nREGRA OBRIGATORIA: responda SEMPRE em português do Brasil, mesmo que a pergunta, "
        "os documentos ou o contexto estejam em outro idioma. Só use outro idioma se o usuário "
        "pedir explicitamente uma tradução ou resposta em outra língua. Não use emojis."
    )

settings = Settings()

# Ensure directories exist
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "data", "documents"), exist_ok=True)

# Para forçar o modo 100% offline DEPOIS do primeiro download, descomente a linha abaixo:
# os.environ["HF_HUB_OFFLINE"] = "1"
