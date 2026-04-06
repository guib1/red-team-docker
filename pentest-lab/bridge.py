#!/usr/bin/env python3
import subprocess
import sys

def run_hexstrike(cmd_args):
    """Executa o HexStrike e retorna a saída para o Gemini"""
    base_cmd = ["python3", "/opt/hexstrike/HexStrike.py"]
    full_cmd = base_cmd + cmd_args
    
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Erro ao executar HexStrike: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_hexstrike(sys.argv[1:]))
    else:
        print("Uso: hex-bridge [argumentos do hexstrike]")
