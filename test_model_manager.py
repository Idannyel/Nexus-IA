"""Suite de testes automatizados para integração de modelos, hardware e Ollama no Nexus IA."""

import os
import sys
import unittest
from unittest.mock import patch

# Ajusta path para importar módulos do Nexus IA
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.model_manager import ModelManager, MODEL_CATALOG
from core.orchestrator import AgentOrchestrator


class TestModelManager(unittest.TestCase):
    """Testes unitários para o gerenciador de modelos e inspeção de recursos."""

    def setUp(self):
        self.manager = ModelManager()

    def test_hardware_info_structure(self):
        """Verifica se a detecção de hardware retorna as métricas esperadas."""
        hw = self.manager.get_hardware_info()
        self.assertIn("total_ram_gb", hw)
        self.assertIn("avail_ram_gb", hw)
        self.assertIn("free_disk_gb", hw)
        self.assertIn("total_disk_gb", hw)
        self.assertIn("gpu_name", hw)
        self.assertGreater(hw["total_ram_gb"], 0.0)
        self.assertGreater(hw["total_disk_gb"], 0.0)
        print(f"Hardware detectado: RAM {hw['avail_ram_gb']}/{hw['total_ram_gb']} GB | Disco {hw['free_disk_gb']}/{hw['total_disk_gb']} GB | Dispositivo: {hw['gpu_name']}")

    def test_family_detection(self):
        """Testa o mapeamento correto de famílias de modelos por tag."""
        self.assertEqual(self.manager.detect_family("deepseek-r1:1.5b"), "deepseek")
        self.assertEqual(self.manager.detect_family("deepseek-coder:1.3b"), "deepseek")
        self.assertEqual(self.manager.detect_family("dolphin-phi:2.7b"), "dolphin")
        self.assertEqual(self.manager.detect_family("dolphin-mistral:7b"), "dolphin")
        self.assertEqual(self.manager.detect_family("gemma3:latest"), "gemma")
        self.assertEqual(self.manager.detect_family("llama3.2:latest"), "llama")
        self.assertEqual(self.manager.detect_family("mistral:7b"), "mistral")
        self.assertEqual(self.manager.detect_family("unknown-model-xyz"), "general")

    def test_model_catalog_completeness(self):
        """Verifica se o catálogo de DeepSeek e Dolphin contém variantes válidas e metadados."""
        self.assertIn("deepseek", MODEL_CATALOG)
        self.assertIn("dolphin", MODEL_CATALOG)

        ds = MODEL_CATALOG["deepseek"]
        self.assertGreater(len(ds["variants"]), 0)
        for var in ds["variants"]:
            self.assertTrue(var["tag"].startswith("deepseek"))
            self.assertGreater(var["size_gb"], 0.0)
            self.assertGreater(var["min_ram_gb"], 0.0)

        dol = MODEL_CATALOG["dolphin"]
        self.assertGreater(len(dol["variants"]), 0)
        for var in dol["variants"]:
            self.assertTrue(var["tag"].startswith("dolphin"))
            self.assertGreater(var["size_gb"], 0.0)
            self.assertGreater(var["min_ram_gb"], 0.0)

    def test_compatibility_evaluator(self):
        """Testa a avaliação lógica de compatibilidade com simulação de recursos."""
        # Cenário 1: Espaço insuficiente em disco
        with patch.object(self.manager, "get_hardware_info", return_value={"free_disk_gb": 1.0, "avail_ram_gb": 8.0}):
            eval_res = self.manager.evaluate_compatibility(size_gb=4.7, min_ram_gb=8.0)
            self.assertEqual(eval_res["status"], "error")
            self.assertFalse(eval_res["can_install"])

        # Cenário 2: RAM livre baixa (aviso)
        with patch.object(self.manager, "get_hardware_info", return_value={"free_disk_gb": 10.0, "avail_ram_gb": 2.0}):
            eval_res = self.manager.evaluate_compatibility(size_gb=1.5, min_ram_gb=4.0)
            self.assertEqual(eval_res["status"], "warning")
            self.assertTrue(eval_res["can_install"])

        # Cenário 3: Recursos suficientes (ok)
        with patch.object(self.manager, "get_hardware_info", return_value={"free_disk_gb": 20.0, "avail_ram_gb": 8.0}):
            eval_res = self.manager.evaluate_compatibility(size_gb=1.1, min_ram_gb=2.5)
            self.assertEqual(eval_res["status"], "ok")
            self.assertTrue(eval_res["can_install"])

    def test_model_params_persistence_and_reset(self):
        """Testa a gravação, leitura e restauração de parâmetros de inferência por modelo."""
        test_tag = "test-custom-deepseek"
        # 1. Padrão inicial
        params = self.manager.get_model_params(test_tag)
        self.assertIn("temperature", params)
        self.assertIn("num_predict", params)

        # 2. Salva override customizado
        saved = self.manager.save_model_params(test_tag, {"temperature": 0.15, "num_predict": 1024, "top_p": 0.85})
        self.assertTrue(saved)

        updated = self.manager.get_model_params(test_tag)
        self.assertEqual(updated["temperature"], 0.15)
        self.assertEqual(updated["num_predict"], 1024)
        self.assertEqual(updated["top_p"], 0.85)

        # 3. Restaura padrões
        res = self.manager.reset_model_params(test_tag)
        self.assertNotEqual(res["temperature"], 0.15)

    def test_orchestrator_specialized_directives(self):
        """Verifica se o orquestrador injeta diretrizes específicas para DeepSeek e Dolphin."""
        orch = AgentOrchestrator()

        # Prompt para DeepSeek
        ds_prompt = orch.build_system_prompt("Executivo", model_name="deepseek-r1:1.5b")
        self.assertIn("DIRETRIZ DE RACIOCINIO - DEEPSEEK", ds_prompt)

        # Prompt para Dolphin
        dol_prompt = orch.build_system_prompt("Executivo", model_name="dolphin-phi:2.7b")
        self.assertIn("DIRETRIZ DE CONVERSACAO - DOLPHIN", dol_prompt)

        # Prompt geral
        gen_prompt = orch.build_system_prompt("Executivo", model_name="gemma3:latest")
        self.assertNotIn("DIRETRIZ DE CONVERSACAO - DOLPHIN", gen_prompt)
        self.assertNotIn("DIRETRIZ DE RACIOCINIO - DEEPSEEK", gen_prompt)

    def test_ollama_live_connectivity_and_installed(self):
        """Testa comunicação real com o serviço Ollama local se estiver online."""
        if not self.manager.is_available():
            self.skipTest("Ollama não está ativo localmente em 127.0.0.1:11434.")

        models = self.manager.list_installed_models()
        self.assertIsInstance(models, list)
        print(f"Modelos detectados no Ollama ({len(models)}): {[m['name'] for m in models]}")

        tags = self.manager.get_installed_tags()
        if tags:
            first = tags[0]
            self.assertTrue(self.manager.is_model_installed(first))

    def test_dynamic_model_inference_stream(self):
        """Testa geração real em streaming alternando modelos se houver modelo compatível instalado."""
        if not self.manager.is_available():
            self.skipTest("Ollama não está ativo localmente em 127.0.0.1:11434.")

        tags = self.manager.get_installed_tags()
        if not tags:
            self.skipTest("Nenhum modelo baixado no Ollama para teste de geração.")

        # Prioriza modelo leve testado no hardware (como llama3.2)
        target_model = None
        for candidate in ["llama3.2:latest", "llama3.2", tags[0]]:
            if candidate in tags:
                target_model = candidate
                break
        if not target_model:
            target_model = tags[0]

        orch = AgentOrchestrator()
        print(f"Executando teste de streaming com modelo local '{target_model}'...")

        chunks = []
        try:
            for chunk in orch.process_message(
                user_message="Diga 'OK' em uma única palavra.",
                history=[],
                persona="Técnico",
                use_rag=False,
                use_tools=False,
                model=target_model,
                options={"temperature": 0.1, "num_predict": 30},
            ):
                chunks.append(chunk)

            full = "".join(chunks).strip()
            self.assertTrue(len(full) > 0, "Deveria retornar tokens do modelo")
            print(f"Sucesso! Resposta gerada via streaming ({target_model}): {full}")
        except Exception as e:
            # Em ambientes com restrição de driver Vulkan, registra o motivo
            print(f"Aviso de execução do modelo {target_model}: {e}")
            if "out-of-memory" in str(e).lower() or "vulkan" in str(e).lower():
                self.skipTest(f"Modelo {target_model} requereu mais buffer gráfico do que o disponível.")
            else:
                raise e


if __name__ == "__main__":
    unittest.main()
