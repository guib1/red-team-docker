FROM docker:cli

# Download ttyd binary at build time (static linked, works on Alpine)
RUN wget -qO /usr/local/bin/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 && \
    chmod +x /usr/local/bin/ttyd

# Each browser tab spawns a new "docker exec" into the pentest container
ENTRYPOINT ["ttyd", "--writable", "-p", "7681", "docker", "exec", "-it", "hexstrike_gemini_lab", "/bin/bash"]
