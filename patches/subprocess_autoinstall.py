import subprocess
import shutil
import sys
import os

# Salva referências originais para evitar recursão
_original_run = subprocess.run
_original_Popen = subprocess.Popen

# Mapeamento manual de comandos comuns que divergem do nome do pacote
CMD_TO_PKG = {
    "nc": "netcat-traditional",
    "ncat": "ncat",
    "hydra": "hydra",
    "nikto": "nikto",
    "wfuzz": "python3-wfuzz",
    "searchsploit": "exploitdb",
    "metasploit": "metasploit-framework",
    "ffuf": "ffuf"
}

def _ensure_installed(command):
    """Verifica se o comando existe e tenta instalar de forma inteligente."""
    if not command or not isinstance(command, str) or '/' in command:
        return
    
    # Ignora binários internos e interpretadores já instalados
    if command in ['cd', 'echo', 'ls', 'python', 'python3', 'bash', 'sh', 'git', 'pip', 'pip3']:
        return

    if shutil.which(command):
        return

    print(f"[*] HexStrike Auto-Install: '{command}' não encontrado. Iniciando busca de pacote...", file=sys.stderr)
    
    pkg_name = CMD_TO_PKG.get(command, command)
    
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        
        # 1. Tenta instalar o nome provável do pacote
        print(f"[*] Tentando instalar pacote: {pkg_name}", file=sys.stderr)
        proc = _original_run(["apt-get", "install", "-y", pkg_name], env=env, capture_output=True)
        
        if proc.returncode == 0:
            print(f"[+] '{command}' instalado com sucesso.", file=sys.stderr)
            return

        # 2. Se falhar, tenta atualizar e procurar via apt-file (se disponível) ou apenas update
        print(f"[*] Falha inicial. Atualizando repositórios...", file=sys.stderr)
        _original_run(["apt-get", "update"], env=env, stdout=subprocess.DEVNULL)
        
        proc = _original_run(["apt-get", "install", "-y", pkg_name], env=env, capture_output=True)
        if proc.returncode == 0:
            print(f"[+] '{command}' instalado após update.", file=sys.stderr)
        else:
            # 3. Tenta usar apt-file para encontrar o pacote correto
            print(f"[*] Procurando qual pacote fornece '{command}' via apt-file...", file=sys.stderr)
            search = _original_run(["apt-file", "search", f"bin/{command}"], capture_output=True, text=True)
            if search.stdout:
                possible_pkgs = [line.split(':')[0] for line in search.stdout.split('\n') if line]
                if possible_pkgs:
                    print(f"[-] Falha ao instalar automaticamente. Sugestão para a IA: O comando '{command}' pode ser encontrado nos pacotes: {', '.join(set(possible_pkgs[:3]))}. Tente 'apt-get install [pacote]'.", file=sys.stderr)
            else:
                print(f"[-] Erro: Comando '{command}' não encontrado nos repositórios Debian.", file=sys.stderr)
                print(f"[*] Sugestão para a IA: Verifique repositórios externos ou instale manualmente via 'git clone'.", file=sys.stderr)
                print(f"[*] Repositórios Úteis: \n - Kali Packages: https://pkg.kali.org/pkg/{command} \n - GitHub: https://github.com/search?q={command}+tool \n - Exploit-DB: https://www.exploit-db.com/", file=sys.stderr)

    except Exception as e:
        print(f"[-] Erro crítico no auto-install: {e}", file=sys.stderr)

def patched_run(*args, **kwargs):
    args_list = list(args)
    cmd_args = args_list[0] if args_list else kwargs.get('args')
    
    if isinstance(cmd_args, list) and len(cmd_args) > 0:
        _ensure_installed(cmd_args[0])
    elif isinstance(cmd_args, str) and not kwargs.get('shell'):
        _ensure_installed(cmd_args)
    
    return _original_run(*args, **kwargs)

# Aplicando Patch no módulo subprocess
subprocess.run = patched_run
subprocess.Popen = lambda *a, **k: (_ensure_installed(a[0][0] if isinstance(a[0], list) else a[0]), _original_Popen(*a, **k))[1]

print("[*] HexStrike Subprocess Patch Ativado.", file=sys.stderr)
