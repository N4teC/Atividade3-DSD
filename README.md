# Jogo da Velha Multiplayer com gRPC
## Atividade 3 - Sistemas Distribuídos

Este projeto implementa um **jogo da velha multiplayer** utilizando **gRPC** como tecnologia de comunicação, desenvolvido como estudo de caso para demonstrar a transmissão de dados e interoperabilidade entre diferentes linguagens de programação.

## 📋 Sobre a Atividade

**Meta:** Implementar, por meio de um estudo de caso, a transmissão de dados com gRPC

**Regras atendidas:**
- ✅ **Transmissão com gRPC**: Toda comunicação é feita através de gRPC com streams bidirecionais
- ✅ **Duas linguagens diferentes**: Servidor em Python e clientes em Python e Ruby
- ✅ **Arquitetura demonstrada**: Arquitetura cliente-servidor com documentação detalhada
- ✅ **Projeto no GitHub**: Código versionado e disponível publicamente

**Estudo de caso escolhido:** Implementação de um jogo simples entre players remotos (jogo da velha multiplayer)

## 🎯 O que foi Implementado

Este projeto demonstra um **jogo da velha multiplayer** em tempo real onde:

- **Servidor Python** gerencia a lógica do jogo e estado do tabuleiro
- **Clientes** podem ser escritos em **Python** ou **Ruby**, demonstrando interoperabilidade
- **Comunicação em tempo real** através de streams bidirecionais gRPC
- **Sincronização automática** entre jogadores
- **Validação de jogadas** no lado servidor
- **Interface de linha de comando** limpa e intuitiva

### Funcionalidades Principais

- 🎮 **Jogo multiplayer**: Dois jogadores remotos podem jogar simultaneamente
- 🔄 **Tempo real**: Atualizações instantâneas do tabuleiro para ambos os jogadores
- 🌐 **Multi-linguagem**: Clientes em Python e Ruby podem interagir sem problemas
- ✅ **Validação**: Jogadas inválidas são rejeitadas automaticamente
- 🏆 **Detecção de vitória**: Identifica vencedor ou empate automaticamente
- 🔒 **Controle de acesso**: Limita exatamente 2 jogadores por partida

## 🏗️ Arquitetura do Sistema

O projeto segue uma **arquitetura Cliente-Servidor** com as seguintes características:

```
┌──────────────────┐    gRPC Stream     ┌───────────────────┐
│  Cliente Python  │ ◄─────────────────►│                   │
│     (Player 1)   │   Bidirectional    │  Servidor Python  │
└──────────────────┘                    │   (Game Logic)    │
                                        │                   │
┌──────────────────┐    gRPC Stream     │                   │
│  Cliente Ruby    │ ◄─────────────────►│                   │
│     (Player 2)   │   Bidirectional    └───────────────────┘
└──────────────────┘
```

### Componentes da Arquitetura

**📡 Servidor (Python)**
- Gerencia o estado global do jogo
- Valida todas as jogadas
- Sincroniza atualizações entre clientes
- Implementa a lógica de vitória/empate
- Utiliza threading para concorrência

**💻 Clientes (Python & Ruby)**
- Interface com o usuário
- Envio de jogadas via gRPC
- Recebimento de atualizações em tempo real
- Renderização do tabuleiro

**📋 Protocol Buffers**
- Define o contrato de comunicação
- Garante consistência entre linguagens
- Especifica mensagens e serviços

### Tecnologias Utilizadas

* **🚀 gRPC**: Framework de comunicação com streams bidirecionais
* **📦 Protocol Buffers**: Serialização de dados e definição de contratos
* **🐍 Python**: Linguagem do servidor e um dos clientes
* **💎 Ruby**: Linguagem do segundo cliente (demonstra interoperabilidade)
* **🧵 Threading**: Gerenciamento de concorrência no servidor
* **📚 Queue**: Sincronização de mensagens entre threads

## 📁 Estrutura do Projeto

```
📂 Atividade3-DSD/
├── 🐍 server.py                    # Servidor do jogo (Python)
├── 🐍 client.py                    # Cliente Python
├── 💎 client.rb                    # Cliente Ruby
├── 📋 tictactoe.proto              # Contrato gRPC (Protocol Buffers)
├── 🔧 tictactoe_pb2.py             # Código Python gerado (mensagens)
├── 🔧 tictactoe_pb2_grpc.py        # Código Python gerado (serviços)
├── 🔧 tictactoe_pb.rb              # Código Ruby gerado (mensagens)
├── 🔧 tictactoe_services_pb.rb     # Código Ruby gerado (serviços)
├── 📦 requirements.txt             # Dependências Python
├── 📦 Gemfile                      # Dependências Ruby
├── 📦 Gemfile.lock                 # Versões fixas das dependências Ruby
├── 📖 README.md                    # Documentação do projeto
└── 📂 __pycache__/                 # Cache Python
    ├── tictactoe_pb2.cpython-*.pyc
    └── tictactoe_pb2_grpc.cpython-*.pyc
```

### Descrição dos Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `server.py` | Servidor principal que gerencia a lógica do jogo, estado do tabuleiro e coordena a comunicação entre jogadores |
| `client.py` | Cliente em Python que permite ao usuário jogar via linha de comando |
| `client.rb` | Cliente em Ruby que oferece a mesma funcionalidade do cliente Python |
| `tictactoe.proto` | Define o contrato gRPC com mensagens e serviços |
| `tictactoe_pb2*.py` | Código Python gerado automaticamente pelo protoc |
| `tictactoe_*pb.rb` | Código Ruby gerado automaticamente pelo protoc |
| `requirements.txt` | Lista as dependências Python necessárias |
| `Gemfile` | Lista as dependências Ruby necessárias |
| `Gemfile.lock` | Fixa as versões exatas das dependências Ruby para reprodutibilidade |

## 🔧 Detalhes Técnicos

### Protocol Buffers (tictactoe.proto)
```protobuf
service TicTacToe {
  rpc GameStream(stream GameRequest) returns (stream GameStateResponse);
}

message GameRequest {
  int32 player_id = 1; // 0 ou 1
  int32 position = 2;  // Posição (0-8)
}

message GameStateResponse {
  string board = 1;     // Tabuleiro formatado
  string message = 2;   // Mensagens para o jogador
  bool your_turn = 3;   // Se é a vez do jogador
  bool game_over = 4;   // Se o jogo terminou
  string winner = 5;    // Vencedor ou "Empate"
}
```

### Dependências

**Python (requirements.txt):**
- `grpcio>=1.60.0` - Framework gRPC
- `grpcio-tools>=1.60.0` - Ferramentas de compilação
- `protobuf>=4.25.0` - Protocol Buffers

**Ruby (Gemfile):**
- `grpc ~> 1.60` - Framework gRPC para Ruby  
- `grpc-tools ~> 1.60` - Ferramentas de compilação Ruby


## 🛠️ Pré-requisitos e Instalação

### Requisitos do Sistema

- **Python** 3.8+ com `pip`
- **Ruby** 2.7+ com `gem` e `bundle`
- **Git** (para clonar o repositório)

### 📥 Instalação das Dependências

#### Opção 1: Configuração Automática (Recomendada)

Se estiver usando **GitHub Codespaces** ou **Dev Containers**, as dependências são instaladas automaticamente.

#### Opção 2: Instalação Manual

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd Atividade3-DSD
```

2. **Instale as dependências Python:**
```bash
pip install -r requirements.txt
```

3. **Instale as dependências Ruby:**
```bash
bundle install
```

### 🔧 Compilação dos Arquivos Protocol Buffers

**⚠️ Importante:** Os arquivos `.pb2.py` e `_pb.rb` já estão incluídos no repositório. Apenas execute os comandos abaixo se precisar recompilar:

```bash
# Gerar código Python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tictactoe.proto

# Gerar código Ruby  
grpc_tools_ruby_protoc -I. --ruby_out=. --grpc_out=. tictactoe.proto
```

## 🎮 Como Executar e Jogar

Para jogar, você precisará de **3 terminais** abertos no diretório do projeto:

### Passo 1: 🖥️ Inicie o Servidor

No **primeiro terminal**, execute o servidor Python:

```bash
python server.py
```

**Saída esperada:**
```
Servidor gRPC rodando na porta 50051.
```

O servidor ficará aguardando as conexões dos jogadores.

### Passo 2: 🎮 Conecte o Primeiro Jogador (X)

No **segundo terminal**, inicie um cliente. Este será o **Jogador 1 (X)**:

**Cliente Ruby:**
```bash
ruby client.rb
```

**OU Cliente Python:**
```bash
python client.py
```

**Saída esperada:**
```
Conectado ao servidor!
Você é o jogador X (0)
Aguardando o segundo jogador se conectar...
```

### Passo 3: 🎯 Conecte o Segundo Jogador (O) e Comece a Jogar

No **terceiro terminal**, inicie outro cliente. Este será o **Jogador 2 (O)**:

```bash
ruby client.rb
# OU
python client.py
```

**O jogo começará automaticamente!**

### 🕹️ Como Jogar

1. **Posições do tabuleiro:**
```
  0 | 1 | 2
 ---+---+---
  3 | 4 | 5
 ---+---+---
  6 | 7 | 8
```

2. **Quando for sua vez:**
   - Aparecerá: `Sua vez, digite a posição (0-8):`
   - Digite um número de **0 a 8** e pressione `Enter`

3. **Atualizações em tempo real:**
   - O tabuleiro é atualizado automaticamente para ambos os jogadores
   - Mensagens indicam de quem é a vez
   - Jogadas inválidas são rejeitadas

4. **Fim do jogo:**
   - O jogo termina quando alguém vence ou há empate
   - Uma mensagem final é exibida para ambos os jogadores

### 📺 Exemplo de Partida

```
Conectado ao servidor!
Você é o jogador X (0)

  _ | _ | _
 ---+---+---
  _ | _ | _
 ---+---+---
  _ | _ | _

Sua vez, digite a posição (0-8): 4

  _ | _ | _
 ---+---+---
  _ | X | _
 ---+---+---
  _ | _ | _

Aguardando jogada do oponente...

  _ | O | _
 ---+---+---
  _ | X | _
 ---+---+---
  _ | _ | _

Sua vez, digite a posição (0-8): 
```

---

* **Desenvolvido por:** Agnes Barbosa e Nathan Cavalcante
* **Disciplina:** Desenvolvimento de Sistemas Distribuídos
* **Professor:** Gracon Lima
* **Semestre:** 2025.1  
