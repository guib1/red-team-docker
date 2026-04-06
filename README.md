# Red Team Docker: AI-Powered Pentest Intelligence

[**Português 🇧🇷**](#português) | [**English 🇺🇸**](#english)

---

<a name="português"></a>
## 🇧🇷 Português

O **Red Team Docker** é um laboratório ofensivo conteinerizado de última geração. Ele combina o poder do **Gemini-AI** com ferramentas de rede de baixo nível, oferecendo uma interface visual (HUD) em tempo real para monitorar sua infraestrutura de ataque.

### 🌟 Novas Funcionalidades (V2.0)
- **Hacker Dashboard (HUD):** Interface web centralizada com estatísticas do Docker em tempo real (CPU, Memória, Rede) para cada container.
- **Ambiente GUI Integrado:** Desktop XFCE4 completo acessível diretamente pelo navegador (noVNC).
- **Arsenal Automático:** O sistema detecta comandos ausentes e sugere ou instala os pacotes necessários via MCP.
- **Conectividade Total:** Usa `network_mode: host` para garantir que VPNs e interfaces de rede (como Wi-Fi no Linux) funcionem nativamente dentro do laboratório.

### 📋 Requisitos
Você só precisa de dois componentes instalados no seu host:
1.  **Python 3.x**
2.  **Docker Desktop** (ou Docker Engine no Linux)

### 📥 Instalação e Uso Automático
A maneira mais fácil de começar é usando o script interativo de setup:

1.  Clone o repositório:
    ```bash
    git clone https://github.com/hyskoniho/red-team-docker.git
    cd red-team-docker
    ```
2.  Inicie o laboratório:
    ```bash
    python setup.py
    ```
3.  **Escolha o Modo:**
    -   **Opcão 1 (Simple):** Apenas o terminal do laboratório no CLI.
    -   **Opção 2 (Complete):** Sobe toda a stack GUI + HUD + Dashboards e abre no seu navegador.

---

<a name="english"></a>
## 🇺🇸 English

**Red Team Docker** is a next-generation containerized offensive lab. It blends the processing power of **Gemini-AI** with low-level network tools, providing a real-time visual HUD to monitor your attack infrastructure.

### 🌟 New Features (V2.0)
- **Hacker Dashboard (HUD):** Centralized Web UI with real-time Docker stats (CPU, Memory, Network) for every container in the stack.
- **Integrated GUI Environment:** Full XFCE4 Desktop accessible directly via your browser (noVNC).
- **Automated Arsenal:** The system detects missing commands and suggests or installs required packages via MCP.
- **Full Connectivity:** Uses `network_mode: host` to ensure VPNs and network interfaces (like Wi-Fi in Linux) work natively inside the lab.

### 📋 Requirements
You only need two components installed on your host:
1.  **Python 3.x**
2.  **Docker Desktop** (or Docker Engine on Linux)

### 📥 Automatic Installation & Usage
The easiest way to start is by using the interactive setup script:

1.  Clone the repository:
    ```bash
    git clone https://github.com/hyskoniho/red-team-docker.git
    cd red-team-docker
    ```
2.  Launch the lab:
    ```bash
    python setup.py
    ```
3.  **Choose your Mode:**
    -   **Option 1 (Simple):** Only the lab terminal in your CLI.
    -   **Option 2 (Complete):** Deploys the full GUI + HUD + Dashboard stack and opens it in your browser.

---

### 🖥️ Dashboard & GUI
Se você escolheu a **Instalação Completa**, o HUD estará disponível abrindo o arquivo `frontend/index.html` ou acessando os serviços individuais:
- **GUI Desktop:** [http://localhost:6080](http://localhost:6080)
- **Terminal Web:** [http://localhost:7681](http://localhost:7681)
- **Stats Bridge:** [http://localhost:8082/stats](http://localhost:8082/stats)

---

> [!CAUTION]
> **Aviso Legal / Legal Disclaimer:** Este ambiente foi criado estritamente para fins educacionais. / This environment was created strictly for educational purposes.
