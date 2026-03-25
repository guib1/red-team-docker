# Red Team Docker: AI-Powered Pentest Lab

Um ambiente de laboratório ofensivo conteinerizado, integrando o **Gemini CLI** com o **HexStrike-AI** via MCP (Model Context Protocol) de forma pré configurada, otimizado para cenários de pentests, ataques simulados e ataques reais (Não incentivamos esse caso).

Este projeto automatiza a configuração de um arsenal de ferramentas de segurança, permitindo que modelos de linguagem (LLMs) executem comandos de infraestrutura e exploração diretamente através do CLI.

Todo o ambiente é rodado por cima do `debian:bookworm-slim` oferecendo um ambiente limpo e leve, a ideia é preparar uma alternativa ao consolidado Kali Linux de forma simples, leve e modular

## 🚀 Funcionalidades

- **Inteligência Artificial Nativa:** Integração profunda com o Gemini CLI para assistência durante pentests.
- **HexStrike-AI Integration:** Configurado como um servidor MCP rodando dentro de uma `screen` para permitir que a IA execute comandos focando menos em ler documentação desnecessária e entregando resultado mais rápido.
- **Instalação automática de ferramentas:** Pré configurado para sempre que chamar o MCP do hexstrike verificar se a ferramenta se encontra instalada no Debian, caso não exista, ele irá instalar automáticamente
- **Persistência de Dados:** Mapeamento de volumes para preservar logs, configurações do Gemini e chaves de API.

## 🛠️ Pré-requisitos

Antes de começar, você precisará de:

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.
- Uma [API Key do Google Gemini](https://aistudio.google.com/app/apikey) ou conta do Google.

## 📥 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/red-team-docker.git
   cd red-team-docker
   ```

2. Configure suas credenciais (**caso for usar API do gemini**):
   Crie um arquivo `.env` na raiz do projeto ou defina a variável de ambiente:
   ```bash
   echo "GEMINI_API_KEY=sua_chave_aqui" > .env
   ```

3. Suba o ambiente:
   ```bash
   docker-compose up -d --build
   ```

## 🖥️ Como Usar

### Acessando o Laboratório

Para entrar no terminal do container interativo:

```bash
docker exec -it hexstrike_gemini_lab /bin/bash
```

Ao entrar, você verá o banner do HexStrike confirmando que as ferramentas e o servidor MCP estão ativos.

### Autenticando o Gemini CLI

Dentro do container, execute o comando inicial para login:

```bash
gemini
```

### Exemplo de Uso com IA

Como o HexStrike está configurado como um servidor MCP, você pode pedir para a IA realizar tarefas diretamente:

```bash
# Dentro do gemini-cli
> "Realize um scan de portas no IP 10.10.10.123 usando o nmap via hexstrike e me mostre vulnerabilidades comuns."
```

### Instalação automática de ferramentas
O sistema tenta instalar automaticamente qualquer ferramenta chamada via HexStrike. Caso a instalação automática falhe:
1. A IA receberá sugestões de pacotes via `apt-file`.
2. Caso o pacote não exista no Debian, a IA receberá links para os repositórios oficiais (Kali, GitHub) para que ela mesma possa realizar o `git clone` e a instalação manual.

### Verificando o Servidor HexStrike
...
O servidor HexStrike roda em background usando `screen`. Você pode visualizar a saída do servidor a qualquer momento:

```bash
screen -r hexstrike
```
*(Para sair do screen sem matar o processo, use `Ctrl+A` seguido de `D`)*.

## 🏗️ Estrutura do Projeto

- `Dockerfile`: Imagem baseada em Debian com Node.js, Python e ferramentas de segurança.
- `docker-compose.yaml`: Gerencia privilégios, volumes e rede.
- `entrypoint.sh`: Automatiza a configuração do MCP no Gemini CLI e inicia os serviços.
- `patches/`: Contém o módulo de "Monkey Patching" para interceptação e auto-instalação de ferramentas.
- `bridge.py`: Script auxiliar para execução de comandos entre a IA e o HexStrike.
- `/workdir`: Pasta persistente para seus códigos e relatórios de pentest.

> [!CAUTION]
> **Aviso Legal:** Este ambiente foi criado estritamente para fins educacionais e de pesquisa em segurança cibernética. O uso dessas ferramentas contra alvos sem autorização prévia é ilegal.
