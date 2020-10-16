from board import Board
from player import Player
from time import sleep
from tkinter import messagebox
from tkinter import PhotoImage
import socket
import threading
import tkinter as tk

window_main = tk.Tk()
window_main.title("Cero mata cero")
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Nombre:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Jugar", command=lambda : join())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)
top_frame = tk.Frame(window_main)

# network client
client = None
CANT_COL = 3
your_turn = False
you_started = False
player1 = Player("player1", "DodgerBlue2", 0, "X")
player2 = Player("player2", "red", 0, "O")
board = Board()

# dibujando el tablero
for x in range(3):
    for y in range(3):
        lbl = tk.Label(top_frame, text=" ", font="Helvetica 45 bold", height=2, width=5, highlightbackground="grey",
                       highlightcolor="grey", highlightthickness=1)
        lbl.bind("<Button-1>", lambda e, xy=[x, y]: get_coordinates(xy))
        lbl.grid(row=x, column=y)

        dict_labels = {"xy": [x, y], "symbol": "", "label": lbl, "ticked": False}
        board.getBoard().append(dict_labels)

lbl_status = tk.Label(top_frame, text="NO esta conectado al servidor", font="Helvetica 14 bold")
lbl_status.grid(row=3, columnspan=3)

top_frame.pack_forget()

def join():
    if len(ent_name.get()) < 1:
        connect_to_server(player1.getName())
    else:
        player1.setName(ent_name.get())
        connect_to_server(ent_name.get())

def connect_to_server(name):
    global client
    PORT = 9000
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("",PORT))
        client.send(name)  # enviar nombre al servidor

        threading.Thread(target=receive_message_from_server, args=(client,)).start()
        top_welcome_frame.pack_forget()
        top_frame.pack(side=tk.TOP)
        window_main.title("Cero mata cero - " + name)
    except Exception as e:
        print('no se pudo conectar al servidor en el puerto' + str(PORT))

def toggle_turn(condition):
    global you_started, your_turn
    you_started = False if condition else True
    your_turn = False if condition else True
    lbl_status["text"] = "Turno de: " + player2.getName() if condition else "Es su turno!"

def init(arg0, arg1):
    sleep(3)
    b = board.getBoard()
    for i in range(len(b)):
        b[i]["symbol"] = ""
        b[i]["ticked"] = False
        b[i]["label"]["text"] = ""
        b[i]["label"].config(foreground="black", highlightbackground="grey",highlightcolor="grey", highlightthickness=1)

    lbl_status.config(foreground="black")
    lbl_status["text"] = "Ya va a empezar el juego"
    sleep(1)

    toggle_turn(you_started)

def result_text(txt, color):
    global lbl_status
    lbl_status["text"] = ""
    lbl_status["text"] = "Se acabo, " + txt + "! Tu(" + str(player1.getScore()) + ") - " \
        "" + player2.getName() + "(" + str(player2.getScore())+")"
    lbl_status.config(foreground=color)
    threading.Thread(target=init, args=("", "")).start()

def get_coordinates(xy):
    global client, your_turn
    # convierte coordenados 2D a 1D
    label_index = xy[0] * CANT_COL + xy[1]
    label = board.getBoard()[label_index]

    if your_turn:
        if label["ticked"] is False:
            label["label"].config(foreground=player1.getColor())
            label["label"]["text"] = player1.getPiece()
            label["ticked"] = True
            label["symbol"] = player1.getPiece()
            # enviar ubicacion en xy al socket
            client.send("~xy~" + str(xy[0]) + "~" + str(xy[1]))
            your_turn = False

            # Se gana o se pierde con el sgte movimiento?
            result = board.status()
            if result[0] is True and result[1] != "": # ganar
                player1.setScore(player1.getScore() + 1)
                result_text("You won", "green")
            elif result[0] is True and result[1] == "":  # empatar
                result_text("Draw", "blue")
            else:
                lbl_status["text"] = "Turno de: " + player2.getName()
    else:
        lbl_status["text"] = "Favor de esperar su turno!"
        lbl_status.config(foreground="red")

def receive_message_from_server(sckt):
    global your_turn, you_started
    while True:
        from_server = sckt.recv(4096)

        if not from_server: break

        if from_server.startswith("player"):
                lbl_status["text"] = ("Bienvenido " + player1.getName() + 
                    "! Esperando por P2" if "1" in from_server else "! Espere un momento")

        elif from_server.startswith("opponent_name~"):
            temp = from_server.replace("opponent_name~", "")
            temp = temp.replace("symbol", "")
            name_index = temp.find("~")
            symbol_index = temp.rfind("~")
            player2.setName(temp[0:name_index])
            player1.setPiece(temp[symbol_index:len(temp)])
            player2.setPiece("X" if player1.getPiece() == "O" else "O")
            lbl_status["text"] = player2.getName() + " se ha conectado!"
            sleep(3)
            toggle_turn(player1.getPiece() == "O")

        elif from_server.startswith("~xy~"):
            temp = from_server.replace("~xy~", "")
            _x = temp[0:temp.find("~")]
            _y = temp[temp.find("~") + 1:len(temp)]

            # actualizar tablero
            label_index = int(_x) * CANT_COL + int(_y)
            label = board.getBoard()[label_index]
            label["symbol"] = player2.getPiece()
            label["label"]["text"] = player2.getPiece()
            label["label"].config(foreground=player2.getColor())
            label["ticked"] = True

            # este cambio hace que el oponente gane/pierda/empate?
            result = board.status()
            if result[0] is True and result[1] != "":  # gano oponente
                player2.setScore(player2.getScore() + 1)
                if result[1] == player2.getPiece():  # perdio oponente
                    result_text("Ha perdido", "red")
            elif result[0] is True and result[1] == "":  # empate
                result_text("Draw", "blue")
            else:
                your_turn = True
                lbl_status["text"] = "Es su turno!"
                lbl_status.config(foreground="black")

    sckt.close()

window_main.mainloop()
