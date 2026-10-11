"""Módulo central de gerenciamento de modelos locais (Ollama) para o Nexus IA.

Suporta:
- Inspeção e detecção de hardware (RAM, Disco, CPU, GPU/VRAM);
- Catálogo especializado com variantes de Dolphin e DeepSeek;
- Consulta ao serviço Ollama (status, modelos instalados, detalhes);
- Download/Pull com acompanhamento de progresso em tempo real;
- Exclusão e liberação de memória (unload) de modelos;
- Gerenciamento de parâmetros específicos por modelo (temperatura, tokens, etc.);
- Avaliação de compatibilidade de recursos antes do download.
"""

import os
import json
import shutil
import ctypes
from typing import Dict, List, Optional, Generator, Any
import ollama

from core.config import settings

# Caminho para persistência de parâmetros customizados por modelo
MODEL_CONFIGS_PATH = os.path.join("data", "model_configs.json")

# Catálogo estruturado multimodelo para o Nexus IA
MODEL_CATALOG = {
    "llama": {
        "id": "llama",
        "name": "Llama (Meta)",
        "badge": "Padrão da Indústria",
        "tagline": "Raciocínio robusto, seguimento de instruções e tarefas gerais.",
        "description": "Modelos da família Llama da Meta AI, amplamente testados e com excelente capacidade geral.",
        "default_params": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": "Você é o assistente Nexus IA baseado em Llama. Seja claro, conciso e profissional.",
        "variants": [
            {
                "tag": "llama3.2:latest",
                "name": "Llama 3.2 (3B)",
                "size_gb": 2.0,
                "min_ram_gb": 4.0,
                "badge": "Recomendado / Balanceado",
                "description": "Excelente equilíbrio entre velocidade e inteligência para tarefas do dia a dia.",
            },
            {
                "tag": "llama3.2:1b",
                "name": "Llama 3.2 (1B)",
                "size_gb": 1.3,
                "min_ram_gb": 2.0,
                "badge": "Ultraleve",
                "description": "Variante supercompacta para respostas instantâneas.",
            },
            {
                "tag": "llama3.1:8b",
                "name": "Llama 3.1 (8B)",
                "size_gb": 4.7,
                "min_ram_gb": 8.0,
                "badge": "Alta Capacidade",
                "description": "Alta capacidade para raciocínio complexo, síntese documental e redação corporativa.",
            },
        ],
    },
    "gemma": {
        "id": "gemma",
        "name": "Gemma (Google)",
        "badge": "Precisão & Síntese",
        "tagline": "Modelos compactos de alta precisão baseados na pesquisa do Google Gemini.",
        "description": "Projetados para tarefas corporativas, síntese estruturada e clareza conceitual.",
        "default_params": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": "Você é o assistente Nexus IA baseado em Gemma. Forneça respostas objetivas e bem fundamentadas.",
        "variants": [
            {
                "tag": "gemma3:latest",
                "name": "Gemma 3 (4B)",
                "size_gb": 3.4,
                "min_ram_gb": 6.0,
                "badge": "Mais Recente",
                "description": "Nova geração de modelos compactos do Google com grande coerência em múltiplos idiomas.",
            },
            {
                "tag": "gemma3:1b",
                "name": "Gemma 3 (1B)",
                "size_gb": 1.0,
                "min_ram_gb": 2.0,
                "badge": "Ultraleve",
                "description": "Ideal para ambientes com baixa memória e alta velocidade.",
            },
            {
                "tag": "gemma2:2b",
                "name": "Gemma 2 (2B)",
                "size_gb": 1.6,
                "min_ram_gb": 3.5,
                "badge": "Eficiente",
                "description": "Arquitetura refinada do Google com alto desempenho em tarefas de texto.",
            },
        ],
    },
    "deepseek": {
        "id": "deepseek",
        "name": "DeepSeek",
        "badge": "Raciocínio & Código",
        "tagline": "Raciocínio lógico, matemática, resolução de problemas e código.",
        "description": (
            "Desenvolvido para análise técnica profunda, raciocínio passo a passo (CoT), "
            "algoritmos, refatoração de código e resolução de problemas lógicos complexos."
        ),
        "default_params": {
            "temperature": 0.6,
            "num_predict": 4096,
            "top_p": 0.95,
        },
        "system_instruction": (
            "Você é um especialista em raciocínio analítico, lógica e engenharia de software. "
            "Pense metodicamente, apresente soluções estruturadas e código limpo e eficiente."
        ),
        "variants": [
            {
                "tag": "deepseek-r1:1.5b",
                "name": "DeepSeek-R1 (1.5B Distill)",
                "size_gb": 1.1,
                "min_ram_gb": 2.5,
                "badge": "Recomendado para CPU / Leve",
                "description": "Variante destilada ultraleve de raciocínio profundo. Execução rápida em CPU e baixo consumo de disco.",
            },
            {
                "tag": "deepseek-coder:1.3b",
                "name": "DeepSeek-Coder (1.3B)",
                "size_gb": 0.8,
                "min_ram_gb": 2.0,
                "badge": "Especialista em Código",
                "description": "Especializado puramente em sintaxe, linguagens de programação e algoritmos com pegada mínima.",
            },
            {
                "tag": "deepseek-r1:7b",
                "name": "DeepSeek-R1 (7B Distill)",
                "size_gb": 4.7,
                "min_ram_gb": 8.0,
                "badge": "Raciocínio Avançado",
                "description": "Excelente poder de raciocínio baseado em Qwen-7B. Requer mais RAM e espaço livre em disco.",
            },
            {
                "tag": "deepseek-r1:8b",
                "name": "DeepSeek-R1 (8B Llama)",
                "size_gb": 4.9,
                "min_ram_gb": 8.0,
                "badge": "Raciocínio Base Llama",
                "description": "Destilado a partir do Llama 3.1 8B. Raciocínio profundo e robusto para tarefas analíticas densas.",
            },
        ],
    },
    "dolphin": {
        "id": "dolphin",
        "name": "Dolphin",
        "badge": "Conversação & Escrita",
        "tagline": "Conversas gerais, escrita criativa, brainstorming e assistência sem filtros.",
        "description": (
            "Projetado para máxima versatilidade, geração de ideias, redação criativa, "
            "diálogos naturais e atendimento a solicitações sem recusas artificiais ou censura desnecessária."
        ),
        "default_params": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": (
            "Você é o assistente Dolphin, prestativo, criativo e multifuncional. "
            "Forneça respostas completas, fluidas, colaborativas e sem barreiras desnecessárias."
        ),
        "variants": [
            {
                "tag": "dolphin-phi:2.7b",
                "name": "Dolphin-Phi (2.7B)",
                "size_gb": 1.6,
                "min_ram_gb": 3.5,
                "badge": "Recomendado para CPU / Leve",
                "description": "Baseado no Phi-2 da Microsoft ajustado por Eric Hartford. Ágil, inteligente e com tamanho compacto.",
            },
            {
                "tag": "dolphin-mistral:7b",
                "name": "Dolphin-Mistral (7B)",
                "size_gb": 4.1,
                "min_ram_gb": 6.5,
                "badge": "Alta Coerência",
                "description": "Variante clássica e aclamada com alta capacidade de argumentação, redação e versatilidade.",
            },
            {
                "tag": "dolphin-llama3:8b",
                "name": "Dolphin-Llama3 (8B)",
                "size_gb": 4.7,
                "min_ram_gb": 8.0,
                "badge": "Topo de Linha",
                "description": "Baseado no Llama 3 8B. Alto desempenho em tarefas complexas, redação corporativa e síntese.",
            },
        ],
    },
    "qwen": {
        "id": "qwen",
        "name": "Qwen (Alibaba)",
        "badge": "Multilíngue & Lógica",
        "tagline": "Excelente suporte a código, matemática e contexto alargado.",
        "description": "Família Qwen 2.5 com altíssimo desempenho em benchmarks abertos de raciocínio.",
        "default_params": {
            "temperature": 0.6,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": "Você é o assistente Nexus IA baseado em Qwen. Responda com rigor técnico e clareza.",
        "variants": [
            {
                "tag": "qwen2.5:1.5b",
                "name": "Qwen 2.5 (1.5B)",
                "size_gb": 1.0,
                "min_ram_gb": 2.0,
                "badge": "Ultraleve",
                "description": "Leve e muito competente em raciocínio básico e instruções simples.",
            },
            {
                "tag": "qwen2.5:3b",
                "name": "Qwen 2.5 (3B)",
                "size_gb": 1.9,
                "min_ram_gb": 4.0,
                "badge": "Balanceado",
                "description": "Capacidade impressionante para seu tamanho em lógica e raciocínio.",
            },
            {
                "tag": "qwen2.5:7b",
                "name": "Qwen 2.5 (7B)",
                "size_gb": 4.7,
                "min_ram_gb": 8.0,
                "badge": "Alta Performance",
                "description": "Excelente compreensão de instruções complexas e raciocínio analítico.",
            },
        ],
    },
    "mistral": {
        "id": "mistral",
        "name": "Mistral (Mistral AI)",
        "badge": "Velocidade & Precisão",
        "tagline": "Eficiência e raciocínio preciso em tarefas de análise textual.",
        "description": "Modelos da Mistral AI com atenção refinada para resposta rápida e objetiva.",
        "default_params": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": "Você é o assistente Nexus IA baseado em Mistral. Forneça respostas diretas e precisas.",
        "variants": [
            {
                "tag": "mistral:7b",
                "name": "Mistral (7B Instruct)",
                "size_gb": 4.1,
                "min_ram_gb": 6.5,
                "badge": "Clássico",
                "description": "Excelente para tarefas executivas, análise de texto e raciocínio.",
            },
        ],
    },
    "general": {
        "id": "general",
        "name": "Geral / Padrão",
        "badge": "Uso Geral",
        "tagline": "Modelos gerais e polivalentes da comunidade.",
        "description": "Modelos comunitários para uso diário no Ollama.",
        "default_params": {
            "temperature": 0.7,
            "num_predict": 2048,
            "top_p": 0.9,
        },
        "system_instruction": "Você é um assistente corporativo prestativo, claro e objetivo.",
        "variants": [],
    },
}


class ModelManager:
    """Gerenciador central de modelos do Ollama para o Nexus IA."""

    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)
        self._ensure_configs_file()

    # ========================== Inspeção de Hardware ==========================

    _cached_gpu_info = None

    @staticmethod
    def get_ollama_storage_path() -> str:
        """Retorna o diretório real onde o Ollama armazena os modelos."""
        custom = os.environ.get("OLLAMA_MODELS")
        if custom and os.path.exists(custom):
            return custom
        user_home = os.path.expanduser("~")
        ollama_default = os.path.join(user_home, ".ollama")
        if os.path.exists(ollama_default):
            return ollama_default
        return os.path.abspath(".")

    @classmethod
    def detect_gpu_device(cls) -> Dict[str, Any]:
        """Detecta acelerador gráfico dedicado (NVIDIA, AMD Radeon, Intel) no Windows ou Linux."""
        if cls._cached_gpu_info is not None:
            return cls._cached_gpu_info

        res = {"has_gpu": False, "gpu_name": "CPU (Processamento local)", "vram_gb": 0.0}

        # 1. Tenta PyTorch CUDA
        try:
            import torch
            if torch.cuda.is_available():
                res["has_gpu"] = True
                res["gpu_name"] = torch.cuda.get_device_name(0)
                res["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 1)
                cls._cached_gpu_info = res
                return res
        except Exception:
            pass

        # 2. No Windows, consulta WMI / CIM para placas AMD Radeon, NVIDIA ou Intel
        if os.name == "nt":
            try:
                import subprocess
                cmd = 'Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM | ConvertTo-Json'
                out = subprocess.check_output(['powershell', '-NoProfile', '-Command', cmd], text=True, timeout=3).strip()
                if out:
                    data = json.loads(out)
                    if isinstance(data, list):
                        data = data[0]
                    name = data.get("Name", "")
                    raw_ram = data.get("AdapterRAM", 0) or 0
                    vram_gb = round(raw_ram / (1024**3), 1)
                    if "6600" in name and (vram_gb == 4.0 or vram_gb == 0.0):
                        vram_gb = 8.0  # AMD RX 6600 possui 8GB VRAM dedicados
                    if name and not any(ign in name.lower() for ign in ["virtual", "basic", "generic"]):
                        res["has_gpu"] = True
                        res["gpu_name"] = name
                        res["vram_gb"] = vram_gb
                        cls._cached_gpu_info = res
                        return res
            except Exception:
                pass

        cls._cached_gpu_info = res
        return res

    @staticmethod
    def get_hardware_info() -> Dict[str, Any]:
        """Detecta especificações de hardware locais (RAM, Disco de modelos, GPU)."""
        info = {
            "total_ram_gb": 0.0,
            "avail_ram_gb": 0.0,
            "free_disk_gb": 0.0,
            "total_disk_gb": 0.0,
            "has_gpu": False,
            "gpu_name": "CPU (Processamento local)",
            "vram_gb": 0.0,
            "ollama_path": "",
        }

        # 1. Memória RAM no Windows via API nativa do Kernel
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                info["total_ram_gb"] = round(stat.ullTotalPhys / (1024**3), 1)
                info["avail_ram_gb"] = round(stat.ullAvailPhys / (1024**3), 1)
        except Exception:
            pass

        # 2. Espaço em Disco (Armazenamento real onde o Ollama salva os modelos)
        try:
            ollama_dir = ModelManager.get_ollama_storage_path()
            disk = shutil.disk_usage(ollama_dir)
            info["free_disk_gb"] = round(disk.free / (1024**3), 1)
            info["total_disk_gb"] = round(disk.total / (1024**3), 1)
            info["ollama_path"] = ollama_dir
        except Exception:
            try:
                disk = shutil.disk_usage(".")
                info["free_disk_gb"] = round(disk.free / (1024**3), 1)
                info["total_disk_gb"] = round(disk.total / (1024**3), 1)
            except Exception:
                pass

        # 3. GPU / Acelerador gráfico dedicado
        gpu_data = ModelManager.detect_gpu_device()
        info["has_gpu"] = gpu_data["has_gpu"]
        info["gpu_name"] = gpu_data["gpu_name"]
        info["vram_gb"] = gpu_data["vram_gb"]

        return info

    def evaluate_compatibility(self, size_gb: float, min_ram_gb: float) -> Dict[str, Any]:
        """Avalia se um modelo é compatível com os recursos atuais da máquina."""
        hw = self.get_hardware_info()
        free_disk = hw["free_disk_gb"]
        avail_ram = hw["avail_ram_gb"]

        # Margem de segurança de disco (precisa do tamanho do download + 500 MB)
        disk_ok = free_disk >= (size_gb + 0.5)
        # Margem de RAM: ideal ter a memória mínima livre
        ram_ok = avail_ram >= min_ram_gb

        if not disk_ok:
            return {
                "status": "error",
                "can_install": False,
                "message": (
                    f"Espaço insuficiente em disco: necessário ~{size_gb:.1f} GB, "
                    f"mas há apenas {free_disk:.1f} GB livres."
                ),
            }
        elif not ram_ok:
            return {
                "status": "warning",
                "can_install": True,
                "message": (
                    f"RAM livre reduzida ({avail_ram:.1f} GB livres, recomendado: {min_ram_gb:.1f} GB). "
                    f"O modelo poderá rodar com maior lentidão na CPU."
                ),
            }
        else:
            return {
                "status": "ok",
                "can_install": True,
                "message": (
                    f"Compatível com o hardware atual ({free_disk:.1f} GB livres em disco, "
                    f"{avail_ram:.1f} GB de RAM livre)."
                ),
            }

    # ========================== Operações no Ollama ==========================

    def is_available(self) -> bool:
        """Verifica se o servidor Ollama está ativo e respondendo localmente."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def list_installed_models(self) -> List[Dict[str, Any]]:
        """Lista os modelos atualmente baixados e instalados no Ollama local."""
        try:
            res = self.client.list()
            raw_models = res.get("models", [])
            installed = []
            for m in raw_models:
                name = m.get("name") or m.get("model") or ""
                size_bytes = m.get("size", 0)
                size_gb = round(size_bytes / (1024**3), 2)
                family = self.detect_family(name)
                installed.append({
                    "name": name,
                    "size_gb": size_gb,
                    "family": family,
                    "modified_at": m.get("modified_at", ""),
                    "digest": m.get("digest", "")[:12],
                })
            return installed
        except Exception as e:
            print(f"[ModelManager] Erro ao listar modelos instalados: {e}")
            return []

    def get_installed_tags(self) -> List[str]:
        """Retorna uma lista simples com as tags de modelos instalados."""
        return [m["name"] for m in self.list_installed_models()]

    def is_model_installed(self, model_tag: str) -> bool:
        """Verifica se uma tag específica de modelo já está baixada no Ollama."""
        tags = self.get_installed_tags()
        target = model_tag.lower()
        return any(t.lower() == target or t.lower().startswith(f"{target}:") for t in tags)

    def pull_model_stream(self, model_tag: str) -> Generator[Dict[str, Any], None, None]:
        """Executa o download de um modelo via Ollama reportando progresso em tempo real."""
        # Validação preventiva de disco
        hw = self.get_hardware_info()
        if hw["free_disk_gb"] < 1.0:
            yield {
                "status": "error",
                "message": f"Espaço em disco insuficiente ({hw['free_disk_gb']:.1f} GB livres). Libere espaço antes de baixar.",
            }
            return

        try:
            stream = self.client.pull(model_tag, stream=True)
            for event in stream:
                status = event.get("status", "")
                completed = event.get("completed", 0)
                total = event.get("total", 0)
                percent = round((completed / total * 100), 1) if total > 0 else 0.0

                yield {
                    "status": status,
                    "completed_mb": round(completed / (1024**2), 1),
                    "total_mb": round(total / (1024**2), 1),
                    "percent": percent,
                }
            yield {"status": "success", "percent": 100.0, "message": f"Modelo '{model_tag}' instalado com sucesso!"}
        except Exception as e:
            yield {"status": "error", "message": f"Falha no download de '{model_tag}': {str(e)}"}

    def delete_model(self, model_tag: str) -> bool:
        """Remove um modelo do Ollama para liberar espaço em disco."""
        try:
            self.client.delete(model_tag)
            return True
        except Exception as e:
            print(f"[ModelManager] Erro ao remover modelo '{model_tag}': {e}")
            return False

    def unload_model(self, model_tag: str) -> bool:
        """Descarrega o modelo da memória RAM/VRAM via keep_alive=0."""
        try:
            self.client.generate(model=model_tag, prompt="", keep_alive=0)
            return True
        except Exception:
            return False

    # ========================== Identificação e Catálogo ==========================

    @staticmethod
    def detect_family(model_name: str) -> str:
        """Identifica a família do modelo a partir do seu nome/tag."""
        name_lower = model_name.lower()
        if "deepseek" in name_lower:
            return "deepseek"
        elif "dolphin" in name_lower:
            return "dolphin"
        elif "gemma" in name_lower:
            return "gemma"
        elif "llama" in name_lower:
            return "llama"
        elif "qwen" in name_lower:
            return "qwen"
        elif "mistral" in name_lower:
            return "mistral"
        return "general"

    def get_family_info(self, family_id: str) -> Dict[str, Any]:
        """Retorna os metadados do catálogo para a família especificada."""
        return MODEL_CATALOG.get(family_id, MODEL_CATALOG["general"])

    # ========================== Parâmetros por Modelo ==========================

    def _ensure_configs_file(self):
        """Garante a existência do arquivo de parâmetros customizados."""
        os.makedirs(os.path.dirname(MODEL_CONFIGS_PATH), exist_ok=True)
        if not os.path.exists(MODEL_CONFIGS_PATH):
            with open(MODEL_CONFIGS_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    def get_model_params(self, model_name: str) -> Dict[str, Any]:
        """Obtém os parâmetros de geração configurados para um modelo (com fallback para os padrões da família)."""
        family_id = self.detect_family(model_name)
        defaults = dict(self.get_family_info(family_id)["default_params"])

        try:
            if os.path.exists(MODEL_CONFIGS_PATH):
                with open(MODEL_CONFIGS_PATH, "r", encoding="utf-8") as f:
                    configs = json.load(f)
                    if model_name in configs:
                        defaults.update(configs[model_name])
        except Exception as e:
            print(f"[ModelManager] Erro ao carregar parâmetros de '{model_name}': {e}")

        return defaults

    def save_model_params(self, model_name: str, params: Dict[str, Any]) -> bool:
        """Salva parâmetros de geração específicos para um modelo."""
        try:
            configs = {}
            if os.path.exists(MODEL_CONFIGS_PATH):
                with open(MODEL_CONFIGS_PATH, "r", encoding="utf-8") as f:
                    configs = json.load(f)
            configs[model_name] = params
            with open(MODEL_CONFIGS_PATH, "w", encoding="utf-8") as f:
                json.dump(configs, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[ModelManager] Erro ao salvar parâmetros de '{model_name}': {e}")
            return False

    def reset_model_params(self, model_name: str) -> Dict[str, Any]:
        """Restaura os parâmetros do modelo para os padrões da sua família."""
        family_id = self.detect_family(model_name)
        defaults = dict(self.get_family_info(family_id)["default_params"])
        try:
            if os.path.exists(MODEL_CONFIGS_PATH):
                with open(MODEL_CONFIGS_PATH, "r", encoding="utf-8") as f:
                    configs = json.load(f)
                if model_name in configs:
                    del configs[model_name]
                    with open(MODEL_CONFIGS_PATH, "w", encoding="utf-8") as f:
                        json.dump(configs, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
        return defaults


# Instância global singleton do gerenciador de modelos
model_manager = ModelManager()
