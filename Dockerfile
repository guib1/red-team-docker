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
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalação Global do Gemini CLI Oficial
RUN npm install -g @google/gemini-cli

# 3. Instalação do HexStrike (Corrigido para evitar erro de 'git not found')
WORKDIR /opt
RUN git clone --depth 1 https://github.com/0x4m4/hexstrike-ai.git /opt/hexstrike

WORKDIR /opt/hexstrike
RUN sed -i '/angr/d' requirements.txt && \
    sed -i '/pwntools/d' requirements.txt && \
    sed -i '/bcrypt==4.0.1/d' requirements.txt && \
    pip3 install -r requirements.txt mcp --break-system-packages

# 4. Copia os scripts para o binário
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /root/pentest

RUN echo 'echo -e "\n\033[1;31m========================================\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m[*] HexStrike + Gemini CLI Ambiente Hacker\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;31m========================================\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;32m[+] HexStrike MCP Server: \033[1;33mAtivado\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;32m[+] Ferramentas: nmap, sqlmap, gobuster, etc.\033[0m\n"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] Para iniciar, digite: \033[1;33mgemini-cl login\033[0m"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] O HexStrike ja esta registrado como um servidor MCP!"' >> /root/.bashrc && \
    echo 'echo -e "\033[1;34m[*] Para ver o console do servidor, digite: \033[1;33mscreen -r hexstrike\n\033[0m"' >> /root/.bashrc

CMD ["/usr/local/bin/entrypoint.sh"]
