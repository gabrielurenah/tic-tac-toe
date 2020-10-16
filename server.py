from time import sleep
import socket as s
import threading

socket = None
jugadores = []
nombres = []

def start():
    global socket
    socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket.bind(('', 9000))
    socket.listen(3) 
    threading.Thread(target=handle_client, args=(socket,)).start()

def handle_client(sckt):
    while True:
        if len(jugadores) < 2:
            client, addr = sckt.accept()
            jugadores.append(client)
            threading.Thread(
                target=send_recv_data, 
                args=(client, addr)
            ).start()

def send_recv_data(client_connection, client_ip_addr):
    global socket, jugadores
    client_name = client_connection.recv(4096)

    client_connection.send('player1' if len(jugadores) < 2 else 'player2')
    nombres.append(client_name)

    if len(jugadores) > 1:
        sleep(1)
        jugadores[0].send('opponent_name~' + str(nombres[1]) + 'symbolO')
        jugadores[1].send('opponent_name~' + str(nombres[0]) + 'symbolX')


    while True:
        data = client_connection.recv(4096)
        if not data: break

        if data.startswith("~xy~"):
            # mandar info a jugador 1 o 2, depende quien haya mandado primero
            jugadores[1 if client_connection == jugadores[0] else 0].send(data)

    client_connection.close()

if __name__ == "__main__":
    i = 0
    while True:
        if i == 0:
            i += 1
            start()
        else: 
            pass