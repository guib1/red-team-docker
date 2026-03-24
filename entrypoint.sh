#!/bin/bash
set -e

# Configura o MCP Server do HexStrike para o gemini-cli (Configuração Global no .gemini/settings.json)
GEMINI_GLOBAL_DIR="/root/.gemini"
SETTINGS_FILE="$GEMINI_GLOBAL_DIR/settings.json"

mkdir -p "$GEMINI_GLOBAL_DIR"

if [ ! -f "$SETTINGS_FILE" ]; then
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "mcpServers": {
    "hexstrike": {
      "command": "python3",
      "args": [
        "/opt/hexstrike/hexstrike_mcp.py"
      ]
    }
  }
}
EOF
else
    # Se o arquivo já existe, usamos o node ou python para injetar o mcpServers sem quebrar o resto
    python3 -c "
import json, os
with open('$SETTINGS_FILE', 'r') as f:
    data = json.load(f)
data['mcpServers'] = {
    'hexstrike': {
        'command': 'python3',
        'args': ['/opt/hexstrike/hexstrike_mcp.py']
    }
}
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
fi

# Compatibilidade com versões que buscam em outros diretórios
mkdir -p /root/.config/gemini /root/.config/gemini-terminator
cp "$SETTINGS_FILE" /root/.config/gemini/mcp.json
cp "$SETTINGS_FILE" /root/.config/gemini-terminator/mcp.json

# Cria o diretório .gemini para evitar erros do gemini-cli
mkdir -p /root/.gemini

# Inicia o servidor HTTP do HexStrike em uma sessão detached do Screen
echo "[*] Iniciando HexStrike Server em background (screen)..."
screen -dmS hexstrike python3 /opt/hexstrike/hexstrike_server.py
sleep 5

# Inicia o bash para interatividade
exec /bin/bash
