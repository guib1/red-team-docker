# Red Team Docker: AI-Powered Pentest Lab

[**Português 🇧🇷**](#português) | [**English 🇺🇸**](#english)

---

<a name="português"></a>
## 🇧🇷 Português

Um ambiente de laboratório ofensivo conteinerizado, integrando o **Gemini CLI** com o **HexStrike-AI** via MCP (Model Context Protocol).

### 🚀 Funcionalidades
- **Inteligência Artificial Nativa:** Integração profunda com o Gemini CLI.
- **Resiliência de Arsenal (Auto-Install):** O sistema detecta comandos ausentes e tenta instalar os pacotes automaticamente. Se falhar, sugere o pacote correto ou fornece links para instalação manual.
- **Persistência de Dados:** Mapeamento de volumes para preservar logs e chaves de API.

### 📥 Instalação
1. `git clone https://github.com/seu-usuario/red-team-docker.git`
2. `cd red-team-docker`
3. `docker-compose up -d --build`

### 🖥️ Como Usar
Para entrar no container:
```bash
docker exec -it hexstrike_gemini_lab /bin/bash
```

#### Autenticando o Gemini
Execute:
```bash
gemini
```
> [!IMPORTANT]
> **Nota sobre Docker:** Na primeira execução, após configurar sua conta, o teclado pode parar de responder. Basta sair do container (`exit` ou `Ctrl+D`) e entrar novamente.

---

<a name="english"></a>
## 🇺🇸 English

A containerized offensive lab environment, integrating **Gemini CLI** with **HexStrike-AI** via MCP (Model Context Protocol).

### 🚀 Features
- **Native AI Intelligence:** Deep integration with Gemini CLI.
- **Arsenal Resilience (Auto-Install):** Automatically detects missing commands and attempts to install them via `apt`. If it fails, it suggests the correct package or provides repository links.
- **Data Persistence:** Volume mapping to preserve logs and API keys.

### 📥 Installation
1. `git clone https://github.com/your-user/red-team-docker.git`
2. `cd red-team-docker`
3. `docker-compose up -d --build`

### 🖥️ How to Use
To enter the container:
```bash
docker exec -it hexstrike_gemini_lab /bin/bash
```

#### Authenticating Gemini
Run:
```bash
gemini
```
> [!IMPORTANT]
> **Docker Note:** On the first run, after setting up your account, the keyboard might stop responding. Simply exit the container (`exit` or `Ctrl+D`) and enter again.

---

### DEMO
[![asciicast](https://asciinema.org/a/g9iQhrANovsVpQAm.svg)](https://asciinema.org/a/g9iQhrANovsVpQAm)

> [!CAUTION]
> **Aviso Legal / Legal Disclaimer:** Este ambiente foi criado estritamente para fins educacionais. / This environment was created strictly for educational purposes.
