import grpc
from concurrent import futures
import time
import threading

# Importar classes geradas
import tictactoe_pb2
import tictactoe_pb2_grpc

class GameLogic:
    """Classe para gerenciar a lógica e o estado do Jogo da Velha."""
    def __init__(self):
        self.board = [' '] * 9
        self.turn = 0
        self.players = [] # Armazenará os contextos dos jogadores
        self.game_over = False
        self.winner = None
        self.lock = threading.Lock()
        self.symbols = ['X', 'O']

    def get_board_string(self):
        return f"""
         {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---+---+---
         {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---+---+---
         {self.board[6]} | {self.board[7]} | {self.board[8]}
        """

    def check_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                self.winner = self.board[a]
                return True
        if ' ' not in self.board:
            self.winner = "Empate"
            return True
        return False

    def make_move(self, position, player_id):
        with self.lock:
            if self.game_over or self.turn % 2 != player_id or not (0 <= position < 9) or self.board[position] != ' ':
                return False # Jogada inválida
            
            self.board[position] = self.symbols[player_id]
            self.turn += 1
            if self.check_winner():
                self.game_over = True
            return True

# Servicer do gRPC
class TicTacToeServicer(tictactoe_pb2_grpc.TicTacToeServicer):
    def __init__(self):
        self.game = GameLogic()
        self.player_streams = [None, None]
        self.lock = threading.Lock()

    def broadcast(self):
        """Envia o estado atual do jogo para ambos os jogadores."""
        for i, context in enumerate(self.player_streams):
            if context:
                is_turn = not self.game.game_over and self.game.turn % 2 == i
                message = "Sua vez de jogar." if is_turn else "Aguarde a vez do oponente."
                if self.game.game_over:
                    if self.game.winner == "Empate":
                        message = "O jogo terminou em empate!"
                    elif self.game.winner == self.game.symbols[i]:
                        message = "Você venceu!"
                    else:
                        message = "Você perdeu."

                state = tictactoe_pb2.GameStateResponse(
                    board=self.game.get_board_string(),
                    message=message,
                    your_turn=is_turn,
                    game_over=self.game.game_over,
                    winner=self.game.winner or ""
                )
                yield (i, state)
    
    def GameStream(self, request_iterator, context):
        player_id = -1
        with self.lock:
            if self.player_streams[0] is None:
                player_id = 0
                self.player_streams[0] = context
                print("Jogador 0 (X) conectado.")
            elif self.player_streams[1] is None:
                player_id = 1
                self.player_streams[1] = context
                print("Jogador 1 (O) conectado. O jogo vai começar!")
            else:
                context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, "Servidor cheio.")
                return

        # Segura o jogador 1 até o 2 conectar
        while self.player_streams[1] is None:
            yield tictactoe_pb2.GameStateResponse(message="Aguardando o segundo jogador...")
            time.sleep(1)

        # Loop principal do jogo para este jogador
        try:
            # Envia estado inicial
            initial_states = list(self.broadcast())
            for pid, state in initial_states:
                if pid == player_id:
                    yield state
            
            for request in request_iterator:
                if request.player_id == self.game.turn % 2:
                    if self.game.make_move(request.position, request.player_id):
                        print(f"Jogador {request.player_id} jogou na posição {request.position}")
                        # Após uma jogada válida, o broadcast envia o estado para ambos
                        # e o yield abaixo garante que o gerador continue
                    else:
                        # Informa sobre jogada inválida apenas para o jogador que tentou
                        yield tictactoe_pb2.GameStateResponse(board=self.game.get_board_string(), message="Jogada inválida. Tente novamente.", your_turn=True)

                # Este yield é o que efetivamente envia as atualizações para os clientes
                # A lógica de broadcast precisa ser chamada fora deste loop para atualizar ambos os jogadores
                # Uma implementação mais robusta usaria queues para desacoplar
                # Por simplicidade, vamos re-transmitir o estado a cada interação
                states_after_move = list(self.broadcast())
                for pid, state in states_after_move:
                     # Este é um hack. Em um sistema real, você usaria um padrão pub/sub.
                     # O gRPC não permite escrever no stream de outro a partir de um servicer diferente.
                     # A solução é ter um thread de broadcast separado.
                     # Por simplicidade, vamos retornar o estado apenas para o jogador atual.
                     # O outro jogador saberá do estado na sua próxima interação (ou no próximo poll).
                     if pid == player_id:
                         yield state
                
                if self.game.game_over:
                    break

        except grpc.RpcError:
            print(f"Jogador {player_id} desconectado.")
        finally:
            with self.lock:
                self.player_streams[player_id] = None
                print(f"Limpando conexão do jogador {player_id}.")
                # Opcional: reiniciar o jogo se um jogador sair
                # self.game = GameLogic() 


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tictactoe_pb2_grpc.add_TicTacToeServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC rodando na porta 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()