FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/hexstrike:/usr/local/bin:$PATH"

# 1. Instalação de dependências do sistema e Node.js
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    nmap \
    sqlmap \
    gobuster \
    openvpn \
    iputils-ping \
    screen \
    apt-file \
    && apt-file update \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalação Global do Gemini CLI Oficial
RUN npm install -g @google/gemini-cli

# 3. Instalação do HexStrike (Corrigido para evitar erro de 'git not found')
WORKDIR /opt
RUN git clone --depth 1 https://github.com/0x4m4/hexstrike-ai.git /opt/hexstrike

# Injeta o patch apenas nos arquivos que NÃO são o próprio patch
COPY patches/subprocess_autoinstall.py /opt/hexstrike/subprocess_autoinstall.py
RUN find /opt/hexstrike -maxdepth 1 -name "*.py" ! -name "subprocess_autoinstall.py" -exec sed -i '1i import sys; sys.path.append("/opt/hexstrike"); import subprocess_autoinstall' {} +

# Corrige placeholders no JSON do HexStrike (IPADDRESS e caminhos)
RUN sed -i 's|/path/hexstrike_mcp.py|/opt/hexstrike/hexstrike_mcp.py|g' /opt/hexstrike/hexstrike-ai-mcp.json || true && \
    sed -i 's|IPADDRESS|127.0.0.1|g' /opt/hexstrike/hexstrike-ai-mcp.json || true

WORKDIR /opt/hexstrike
RUN pip3 install mcp fastmcp httpx --break-system-packages
RUN sed -i '/angr/d' requirements.txt && \
    sed -i '/pwntools/d' requirements.txt && \
    sed -i '/bcrypt==4.0.1/d' requirements.txt && \
    pip3 install -r requirements.txt --break-system-packages

# 4. Copia os scripts para o binário e skills do gemini
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh && \
    sed -i 's/\r$//' /usr/local/bin/entrypoint.sh

# Pré-instalação das skills solicitadas
COPY .agents /root/.agents
COPY skills-lock.json /root/skills-lock.json

WORKDIR /root/pentest

RUN echo 'echo -e "\n\033[1;31m========================================\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[*] Ambiente Red Team p/ pentests\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m========================================\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;32m[+] HexStrike MCP Server: \033[1;33mAtivado\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;32m[+] Ferramentas: nmap, sqlmap, gobuster, etc.\033[0m\n"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] Para iniciar, digite: \033[1;33mgemini\033[0m (To start, type: \033[1;33mgemini\033[1;34m)"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[!] PT: Na primeira vez, o terminal pode CONGELAR após o login.\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[!] EN: On the first run, the terminal may FREEZE after login.\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[!] Caso aconteça, saia e entre novamente (Ctrl+D / docker exec).\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[!] If it happens, exit and enter again (Ctrl+D / docker exec).\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] HexStrike MCP Server: \033[1;33mAtivado/Active\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] Para ver o console do servidor, digite: \033[1;33mscreen -r hexstrike\n\033[0m"' >> /root/.bashrc

CMD ["/usr/local/bin/entrypoint.sh"]
