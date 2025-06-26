import grpc
import threading
import sys
import os

# Importar as classes geradas pelo gRPC
import tictactoe_pb2
import tictactoe_pb2_grpc

# Variável global para saber o ID do jogador, atribuído pelo servidor
player_id = -1

def clear_screen():
    """Limpa o console para uma exibição mais limpa do tabuleiro."""
    os.system('cls' if os.name == 'nt' else 'clear')

def listen_for_updates(stub, response_iterator):
    """
    Esta função roda em uma thread separada para ouvir continuamente
    as mensagens (GameStateResponse) do servidor.
    """
    global player_id
    try:
        for response in response_iterator:
            # Atribui o ID do jogador na primeira resposta útil do servidor
            if player_id == -1 and '|' in response.board:
                player_id = 0 if response.your_turn else 1
                symbol = 'X' if player_id == 0 else 'O'
                print(f"Você é o jogador {player_id} ({symbol}).")

            clear_screen()
            print("=== JOGO DA VELHA gRPC (Cliente Python) ===")
            print(response.board)
            print(f"\nStatus: {response.message}")

            if response.your_turn and not response.game_over:
                print("Sua vez, digite a posição (0-8): ", end='', flush=True)

            if response.game_over:
                print("FIM DE JOGO!")
                # Sinaliza o fim para o gerador de requisições
                # (uma maneira de fechar a conexão de forma limpa)
                break
                
    except grpc.RpcError as e:
        print(f"Erro de conexão: O servidor pode ter sido encerrado. {e.details()}")
    finally:
        print("Conexão com o servidor perdida.")
        # Força o encerramento do programa principal
        os._exit(1)


def generate_requests():
    """
    Esta função (um gerador) lê a entrada do usuário no console
    e envia para o servidor como uma mensagem GameRequest.
    """
    global player_id
    
    # Envia uma primeira mensagem para se registrar no servidor
    yield tictactoe_pb2.GameRequest(player_id= -1, position=-1)

    while True:
        try:
            # O input() bloqueia a thread principal, aguardando a jogada
            move = input()
            if move.isdigit():
                yield tictactoe_pb2.GameRequest(player_id=player_id, position=int(move))
            else:
                # O loop continua se a entrada não for um dígito
                print("Entrada inválida. Por favor, digite um número de 0 a 8.", end='', flush=True)

        except (EOFError, KeyboardInterrupt):
            print("\nSaindo do jogo.")
            return # Encerra o gerador, fechando o stream do lado do cliente


def run():
    """
    Função principal que configura o gRPC e inicia as threads.
    """
    # Conecta ao servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tictactoe_pb2_grpc.TicTacToeStub(channel)
        print("Conectando ao servidor do Jogo da Velha...")

        # O método GameStream espera um iterador de requisições
        # e retorna um iterador de respostas
        response_iterator = stub.GameStream(generate_requests())

        # Inicia a thread que ouve as atualizações do servidor
        listener_thread = threading.Thread(
            target=listen_for_updates,
            args=(stub, response_iterator),
            daemon=True
        )
        listener_thread.start()

        # Mantém a thread principal viva para que a daemon thread possa rodar
        # A thread principal ficará efetivamente bloqueada pelo input() em generate_requests
        listener_thread.join()


if __name__ == '__main__':
    run()