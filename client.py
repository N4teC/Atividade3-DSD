import socket
import threading
import random

SERVER_IP = 'localhost' #> pode mudar para o IP do servidor
TCP_PORT = 5001
UDP_PORT = random.randint(6000, 7000) 

def udp_listener(udp_port):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', udp_port))
    while True:
        msg, _ = udp_sock.recvfrom(1024)
        print(f"\n{msg.decode()}")

threading.Thread(target=udp_listener, args=(UDP_PORT,), daemon=True).start()

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((SERVER_IP, TCP_PORT))

tcp_sock.sendall(str(UDP_PORT).encode())

while True:
    data = tcp_sock.recv(1024).decode()
    if not data:
        break
    print(data)
    if "posição" in data:
        move = input(">> ")
        tcp_sock.sendall(move.encode())
