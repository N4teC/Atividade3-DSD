import socket, threading, time

HOST = '0.0.0.0'
TCP_PORT = 5001

board = [' '] * 9
turn = 0
players = [] 
symbols = ['X', 'O']
game_over = False

def print_board():
    return f"""
 {board[0]} | {board[1]} | {board[2]} 
---+---+---
 {board[3]} | {board[4]} | {board[5]} 
---+---+---
 {board[6]} | {board[7]} | {board[8]} 
"""

def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),
            (1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != ' ':
            return True
    return False

def handle_client(conn, player_id, udp_sock):
    global turn, game_over

    udp_data = conn.recv(1024).decode()
    udp_port = int(udp_data)
    client_ip = conn.getpeername()[0]
    udp_addr = (client_ip, udp_port)
    players[player_id] = (conn, udp_addr)

    conn.sendall(f"Você é o jogador {symbols[player_id]}\n".encode())

    while not game_over:
        if turn % 2 == player_id:
            conn.sendall("Sua vez. Escolha posição (0-8): ".encode())
            pos = conn.recv(1024).decode().strip()
            if not pos or not pos.isdigit(): continue
            pos = int(pos)

            if 0 <= pos < 9 and board[pos] == ' ':
                board[pos] = symbols[player_id]
                turn += 1

                for p, _ in players:
                    p.sendall(print_board().encode())
                
                if check_winner():
                    game_over = True
                    for i, (p, udp) in enumerate(players):
                        msg = "Você venceu!" if i == player_id else "Você perdeu."
                        udp_sock.sendto(msg.encode(), udp)
                elif ' ' not in board:
                    game_over = True
                    for _, udp in players:
                        udp_sock.sendto("Empate!".encode(), udp)
            else:
                udp_sock.sendto("Jogada inválida!".encode(), udp_addr)
        
        else:
            time.sleep(0.1)

    conn.close()

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((HOST, TCP_PORT))
tcp_sock.listen(2)
print(f"[TCP] Servidor ouvindo em {HOST}:{TCP_PORT}")

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while len(players) < 2:
    conn, addr = tcp_sock.accept()
    print(f"[TCP] Jogador conectado: {addr}")
    players.append((conn, None))

    if len(players) == 1:
        conn.sendall("Aguardando o outro jogador se conectar...\n".encode())
    elif len(players) == 2:
        for p, _ in players:
            p.sendall("Todos os jogadores conectados. O jogo vai começar!\n".encode())

    threading.Thread(target=handle_client, args=(conn, len(players)-1, udp_sock)).start()
