FROM debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1

# Instalar ambiente gráfico + VNC + noVNC
RUN apt update && apt install -y \
    xfce4 xfce4-goodies \
    tigervnc-standalone-server \
    novnc websockify \
    xterm dbus-x11 \
    sudo curl \
    && apt clean

# Criar usuário (evita rodar tudo como root)
RUN useradd -m -s /bin/bash user && \
    echo "user:user" | chpasswd && \
    adduser user sudo

USER user
WORKDIR /home/user

# Configurar VNC senha
RUN mkdir -p /home/user/.vnc && \
    echo "1234" | vncpasswd -f > /home/user/.vnc/passwd && \
    chmod 600 /home/user/.vnc/passwd

# Script de inicialização
RUN echo '#!/bin/bash\n\
export DISPLAY=:1\n\
\n\
# inicia VNC\n\
vncserver :1 -geometry 1280x800 -depth 24\n\
\n\
# inicia noVNC\n\
websockify --web=/usr/share/novnc/ 6080 localhost:5901\n\
' > /home/user/start.sh && chmod +x /home/user/start.sh

EXPOSE 6080

CMD ["/home/user/start.sh"]