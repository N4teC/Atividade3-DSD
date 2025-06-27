# Projeto: Jogo da Velha com gRPC

Este projeto é uma implementação de um jogo da velha multiplayer de linha de comando, desenvolvido para demonstrar a comunicação entre processos utilizando gRPC.

O objetivo principal é demonstrar a comunicação entre processos utilizando gRPC, com um servidor e clientes escritos em linguagens de programação diferentes, mostrando a interoperabilidade e os benefícios dessa tecnologia.

## Arquitetura e Tecnologias

O projeto segue uma arquitetura Cliente-Servidor clássica, onde toda a lógica do jogo e o gerenciamento de estado são centralizados no servidor. Os clientes são responsáveis apenas por exibir o estado do jogo e capturar a entrada do usuário.

* **gRPC:** Utilizado como framework de comunicação. A comunicação é feita através de um stream bidirecional, permitindo que o cliente envie jogadas e o servidor envie atualizações de estado em tempo real de forma contínua e eficiente.
* **Protocol Buffers (Protobuf):** Usado para definir o "contrato" de serviço no arquivo `tictactoe.proto`. Este contrato especifica os métodos remotos e as estruturas das mensagens trocadas.
* **Linguagens:**
    * **Servidor:** Implementado em Python.
    * **Clientes:** Implementados em Ruby e Python, para cumprir o requisito de utilizar duas linguagens diferentes na comunicação.
* **Concorrência:** O servidor utiliza `threading` e `queue` para gerenciar as conexões de múltiplos jogadores e sincronizar as atualizações em tempo real.

## Estrutura do Projeto

```
├── client.py                   # Cliente em Python
├── client.rb                   # Cliente em Ruby
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

### Opção 1: Configuração Automática (Recomendada)

Se você estiver usando GitHub Codespaces ou Dev Containers, as dependências serão instaladas automaticamente quando o ambiente for criado.

Alternativamente, você pode executar o script de setup:

```bash
./setup.sh
```

### Opção 2: Instalação Manual

Se preferir instalar manualmente ou se a configuração automática não funcionar:

```bash
# Instalar dependências do Python
pip install -r requirements.txt

# Instalar dependências do Ruby
bundle install
```

### 2. Compile o Arquivo .proto

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

No segundo terminal, inicie um cliente (Ruby ou Python). Ele será o **Jogador 0 (X)**.

Para usar o cliente Ruby:
```bash
ruby client.rb
```

Para usar o cliente Python:
```bash
python client.py
```

O primeiro jogador se conectará e exibirá uma mensagem de "Aguardando o segundo jogador...".

### Passo 3: Conecte o Segundo Jogador e Jogue

No terceiro terminal, inicie outro cliente (pode ser Ruby ou Python). Ele será o **Jogador 1 (O)**.

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

## Funcionalidades Implementadas

- ✅ **Comunicação bidirecional em tempo real**: Ambos os jogadores recebem atualizações instantâneas sobre o estado do jogo
- ✅ **Interoperabilidade**: Clientes Ruby e Python podem jogar entre si sem problemas
- ✅ **Gerenciamento de estado**: O servidor centraliza toda a lógica do jogo e valida as jogadas
- ✅ **Detecção de vitória e empate**: O jogo detecta automaticamente quando alguém vence ou há empate
- ✅ **Validação de jogadas**: Jogadas inválidas são rejeitadas e o jogador é notificado
- ✅ **Interface limpa**: A tela é limpa automaticamente para melhor experiência visual
- ✅ **Conexão segura**: O servidor permite exatamente 2 jogadores e rejeita conexões extras