import grpc
from concurrent import futures
import time
import threading
import queue

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
        self.player_queues = [queue.Queue(), queue.Queue()]
        self.player_connected = [False, False]
        self.lock = threading.Lock()

    def broadcast_state(self):
        """Envia o estado atual do jogo para ambos os jogadores via suas queues."""
        for i in range(2):
            if self.player_connected[i]:
                is_turn = not self.game.game_over and self.game.turn % 2 == i
                message = "Sua vez, digite a posição (0-8):" if is_turn else "Aguardando a jogada do oponente..."
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
                try:
                    self.player_queues[i].put_nowait(state)
                except queue.Full:
                    pass  # Se a queue estiver cheia, ignora

    def GameStream(self, request_iterator, context):
        player_id = -1
        with self.lock:
            if not self.player_connected[0]:
                player_id = 0
                self.player_connected[0] = True
                print("Jogador 0 (X) conectado.")
            elif not self.player_connected[1]:
                player_id = 1
                self.player_connected[1] = True
                print("Jogador 1 (O) conectado. O jogo vai começar!")
            else:
                context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, "Servidor cheio.")
                return

        try:
            # Se é o jogador 0, aguarda o jogador 1
            if player_id == 0:
                while not self.player_connected[1]:
                    yield tictactoe_pb2.GameStateResponse(message="Aguardando o segundo jogador...")
                    time.sleep(1)

            # Envia estado inicial
            self.broadcast_state()
            
            # Thread para processar entrada do jogador
            def process_moves():
                try:
                    for request in request_iterator:
                        # Ignora mensagem inicial de registro (position -1)
                        if request.position == -1:
                            continue
                            
                        # Verifica se é a vez do jogador correto
                        actual_player_id = player_id if request.player_id == -1 else request.player_id
                        
                        if actual_player_id == self.game.turn % 2:
                            if self.game.make_move(request.position, actual_player_id):
                                print(f"Jogador {actual_player_id} jogou na posição {request.position}")
                                # Notifica ambos os jogadores sobre a jogada
                                self.broadcast_state()
                            else:
                                # Jogada inválida - envia mensagem apenas para este jogador
                                invalid_state = tictactoe_pb2.GameStateResponse(
                                    board=self.game.get_board_string(), 
                                    message="Jogada inválida. Tente novamente.", 
                                    your_turn=True,
                                    game_over=self.game.game_over,
                                    winner=self.game.winner or ""
                                )
                                try:
                                    self.player_queues[player_id].put_nowait(invalid_state)
                                except queue.Full:
                                    pass
                except:
                    pass

            # Inicia thread para processar movimentos
            move_thread = threading.Thread(target=process_moves, daemon=True)
            move_thread.start()
            
            # Loop principal - envia estados da queue
            while not self.game.game_over:
                try:
                    # Aguarda por atualizações na queue deste jogador
                    state = self.player_queues[player_id].get(timeout=2.0)
                    yield state
                    
                except queue.Empty:
                    # Timeout - envia heartbeat para manter conexão
                    continue

        except grpc.RpcError:
            print(f"Jogador {player_id} desconectado.")
        finally:
            with self.lock:
                self.player_connected[player_id] = False
                print(f"Limpando conexão do jogador {player_id}.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tictactoe_pb2_grpc.add_TicTacToeServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC rodando na porta 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()