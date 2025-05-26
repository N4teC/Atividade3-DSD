# Jogo da Velha Multiplayer com TCP e UDP

Este é um projeto simples de **jogo da velha multiplayer (2 jogadores)** usando sockets em Python.

- O servidor gerencia a lógica do jogo usando **TCP para comandos** e **UDP para mensagens de sistema** (vitória ou derrota).
- Cada cliente se conecta via TCP e abre uma porta UDP aleatória para receber mensagens.

---

## Como executar

### 1. Requisitos

- Python 3.10+
- Sistema que permita execução de sockets (Windows/Linux)

### 2. Clonar o projeto

```bash
git clone https://github.com/AgnesGB/Atividade2-DSD
cd Atividade2-DSD
```

### 3. Executar o servidor

```bash
python server.py
```

### 4. Executar dois clientes em terminais diferentes

```bash
python client.py
```

### 5. Jogar!!