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

    # Evita recursão se o comando for apt-get ou apt-file
    if command in ['apt-get', 'apt-file', 'apt']:
        return

    print(f"[*] HexStrike Auto-Install: '{command}' não encontrado. Iniciando busca...", file=sys.stderr)
    
    pkg_name = CMD_TO_PKG.get(command, command)
    
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        
        # 1. Tenta instalar o pacote
        proc = _original_run(["apt-get", "install", "-y", pkg_name], env=env, capture_output=True)
        
        if proc.returncode == 0:
            print(f"[+] '{command}' instalado com sucesso.", file=sys.stderr)
            return

        # 2. Se falhar, tenta atualizar e procurar via apt-file
        _original_run(["apt-get", "update"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        proc = _original_run(["apt-get", "install", "-y", pkg_name], env=env, capture_output=True)
        if proc.returncode == 0:
            print(f"[+] '{command}' instalado após update.", file=sys.stderr)
        else:
            # 3. Tenta usar apt-file
            search = _original_run(["apt-file", "search", f"bin/{command}"], capture_output=True, text=True)
            if search.stdout:
                possible_pkgs = [line.split(':')[0] for line in search.stdout.split('\n') if line]
                if possible_pkgs:
                    print(f"[-] Comando '{command}' pode estar nos pacotes: {', '.join(set(possible_pkgs[:3]))}", file=sys.stderr)
            else:
                print(f"[-] Erro: '{command}' não encontrado nos repositórios.", file=sys.stderr)
                print(f"[*] Verifique: https://pkg.kali.org/pkg/{command}", file=sys.stderr)

    except Exception as e:
        # Silencioso para não quebrar o fluxo principal
        pass

def _extract_command(args):
    """Extrai o comando de forma segura."""
    if isinstance(args, list) and len(args) > 0:
        return args[0]
    if isinstance(args, str):
        return args.split()[0]
    return None

def patched_run(*args, **kwargs):
    cmd_args = args[0] if args else kwargs.get('args')
    cmd = _extract_command(cmd_args)
    if cmd: _ensure_installed(cmd)
    return _original_run(*args, **kwargs)

# Patch via Classe para manter compatibilidade com Type Hinting (Subscriptable Popen)
class PatchedPopen(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        cmd_args = args[0] if args else kwargs.get('args')
        cmd = _extract_command(cmd_args)
        if cmd: _ensure_installed(cmd)
        super().__init__(*args, **kwargs)

# Aplicando Patches
subprocess.run = patched_run
subprocess.Popen = PatchedPopen
subprocess.call = lambda *a, **k: (_ensure_installed(_extract_command(a[0] if a else k.get('args'))), _original_run(*a, **k).returncode)[1]

print("[*] HexStrike Subprocess Patch Ativado (Class-Based).", file=sys.stderr)
