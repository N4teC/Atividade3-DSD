# Projeto: Jogo da Velha com gRPC

Este projeto é uma implementação de um jogo da velha multiplayer de linha de comando, desenvolvido para a Tarefa 4 da disciplina de Sistemas Distribuídos.

O objetivo principal é demonstrar a comunicação entre processos utilizando gRPC, com um servidor e um cliente escritos em linguagens de programação diferentes, mostrando a interoperabilidade e os benefícios dessa tecnologia.

## Arquitetura e Tecnologias

O projeto segue uma arquitetura Cliente-Servidor clássica, onde toda a lógica do jogo e o gerenciamento de estado são centralizados no servidor. Os clientes são responsáveis apenas por exibir o estado do jogo e capturar a entrada do usuário.

* **gRPC:** Utilizado como framework de comunicação. A comunicação é feita através de um stream bidirecional, permitindo que o cliente envie jogadas e o servidor envie atualizações de estado em tempo real de forma contínua e eficiente.
* **Protocol Buffers (Protobuf):** Usado para definir o "contrato" de serviço no arquivo `tictactoe.proto`. Este contrato especifica os métodos remotos e as estruturas das mensagens trocadas.
* **Linguagens:**
    * **Servidor:** Implementado em Python.
    * **Cliente:** Implementado em Ruby, para cumprir o requisito de utilizar duas linguagens diferentes na comunicação.
* **Concorrência:** O servidor utiliza `threading` para gerenciar as conexões de múltiplos jogadores de forma segura.

## Estrutura do Projeto

```
├── client.py                   # Cliente alternativo em Python (para testes)
├── client.rb                   # Cliente principal em Ruby
├── server.py                   # Servidor do jogo em Python
├── tictactoe.proto             # Arquivo de definição do serviço (contrato)
├── tictactoe_pb2.py            # Código Python gerado pelo protoc
├── tictactoe_pb2_grpc.py       # Código Python gerado pelo protoc
├── tictactoe_pb.rb             # Código Ruby gerado pelo protoc
└── tictactoe_services_pb.rb    # Código Ruby gerado pelo protoc
```

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

* Python (versão 3.8 ou superior) e o gerenciador de pacotes `pip`.
* Ruby (versão 2.7 ou superior) e o gerenciador de pacotes `gem`.

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e instalar as dependências.

### 1. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
```

### 2. Instale as Dependências (Python e Ruby)

```bash
# Instalar dependências do Python
pip install grpcio grpcio-tools

# Instalar dependências do Ruby
gem install grpc grpc-tools
```

### 3. Compile o Arquivo .proto

```bash
# Gerar código para Python
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tictactoe.proto

# Gerar código para Ruby
grpc_tools_ruby_protoc -I. --ruby_out=. --grpc_out=. tictactoe.proto
```

## Como Rodar e Jogar

Para jogar, você precisará de 3 janelas de terminal abertas no diretório do projeto.

### Passo 1: Inicie o servidor

Em um terminal, execute o servidor Python. Ele ficará aguardando as conexões dos jogadores.

```bash
python server.py
```

Você deverá ver a mensagem: `Servidor gRPC rodando na porta 50051.`

### Passo 2: Conecte o primeiro jogador

No segundo terminal, inicie o cliente (Ruby ou Python). Ele será o **Jogador 0 (X)**.

```bash
ruby client.rb

# ou

python client.py
```

Ele se conectará e exibirá uma mensagem de "Aguardando o segundo jogador...".

### Passo 3: Conecte o Segundo Jogador e Jogue

No terceiro terminal, inicie outro cliente. Ele será o **Jogador 1 (O)**.

Assim que o segundo jogador se conectar, o jogo começará no terminal do primeiro jogador.

### Para jogar:

* Quando for a sua vez, o terminal exibirá a mensagem: `Sua vez, digite a posição (0-8):`.
* Digite um número de 0 a 8 correspondente à posição no tabuleiro e pressione `Enter`.

```
  0 | 1 | 2
 ---+---+---
  3 | 4 | 5
 ---+---+---
  6 | 7 | 8
```

* O tabuleiro será atualizado para ambos os jogadores a cada jogada. O jogo termina quando um jogador vence ou ocorre um empate.
