FROM python:3.11-slim

RUN pip install websockify && \
    apt-get update && apt-get install -y novnc && \
    rm -rf /var/lib/apt/lists/*

# Connect to VNC on localhost:5901 (works because this container also uses host network)
# websockify proxies WebSocket (6080) -> TCP (VNC 5901)
ENTRYPOINT ["websockify", "--web=/usr/share/novnc/", "6080", "localhost:5901"]
