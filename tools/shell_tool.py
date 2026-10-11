import subprocess

class ShellTool:
    def execute(self, command: str) -> str:
        """Executa um comando no shell local de forma segura."""
        # TODO: Adicionar sandboxing ou bloqueio de comandos perigosos (rm -rf, mkfs, etc)
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Erro na execução (Código {result.returncode}):\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Erro: O comando excedeu o tempo limite de execução (30s)."
        except Exception as e:
            return f"Erro inesperado: {str(e)}"
