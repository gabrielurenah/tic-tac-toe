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

CANT_COL = 3
your_turn = False
you_started = False
player1 = Player("player1", "DodgerBlue2", 0, "X")
player2 = Player("AI", "red", 0, "O")
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

lbl_status = tk.Label(top_frame, text="vs CPU", font="Helvetica 14 bold")
lbl_status.grid(row=3, columnspan=3)

top_frame.pack_forget()

def join():
    player1.setName(ent_name.get())
    top_welcome_frame.pack_forget()
    top_frame.pack(side=tk.TOP)
    window_main.title("Cero mata cero - " + ent_name.get())
    toggle_turn(player1.getPiece() == "O")

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
    global your_turn
    # convierte coordenados 2D a 1D
    label_index = xy[0] * CANT_COL + xy[1]
    label = board.getBoard()[label_index]

    if your_turn:
        if label["ticked"] is False:
            label["label"].config(foreground=player1.getColor())
            label["label"]["text"] = player1.getPiece()
            label["ticked"] = True
            label["symbol"] = player1.getPiece()
            # get best move
            # client.send("~xy~" + str(xy[0]) + "~" + str(xy[1]))
            play_move(xy)
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

def play_move(xy):
  print(xy)
  # actualizar tablero
  label_index = int(xy[0]) * CANT_COL + int(xy[1])
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

def getBestMove(state, player):
    '''
    Minimax Algorithm
    '''
    # winner_loser , done = check_current_state(state)
    # if done == "Done" and winner_loser == 'O': # If AI won
    #     return 1
    # elif done == "Done" and winner_loser == 'X': # If Human won
    #     return -1
    # elif done == "Draw":    # Draw condition
    #     return 0
        
    # moves = []
    # empty_cells = []
    # for i in range(3):
    #     for j in range(3):
    #         if state[i][j] == ' ':
    #             empty_cells.append(i*3 + (j+1))
    
    # for empty_cell in empty_cells:
    #     move = {}
    #     move['index'] = empty_cell
    #     new_state = copy_game_state(state)
    #     play_move(new_state, player, empty_cell)
        
    #     if player == 'O':    # If AI
    #         result = getBestMove(new_state, 'X')    # make more depth tree for human
    #         move['score'] = result
    #     else:
    #         result = getBestMove(new_state, 'O')    # make more depth tree for AI
    #         move['score'] = result
        
    #     moves.append(move)

    # # Find best move
    # best_move = None
    # if player == 'O':   # If AI player
    #     best = -infinity
    #     for move in moves:
    #         if move['score'] > best:
    #             best = move['score']
    #             best_move = move['index']
    # else:
    #     best = infinity
    #     for move in moves:
    #         if move['score'] < best:
    #             best = move['score']
    #             best_move = move['index']
                
    # return best_move

# def receive_message_from_server(sckt):
#     global your_turn, you_started
#     while True:
#         from_server = sckt.recv(4096)

#         if not from_server: break

#         if from_server.startswith("player"):
#                 lbl_status["text"] = ("Bienvenido " + player1.getName() + 
#                     "! Esperando por P2" if "1" in from_server else "! Espere un momento")

#         elif from_server.startswith("opponent_name~"):
#             temp = from_server.replace("opponent_name~", "")
#             temp = temp.replace("symbol", "")
#             name_index = temp.find("~")
#             symbol_index = temp.rfind("~")
#             player2.setName(temp[0:name_index])
#             player1.setPiece(temp[symbol_index:len(temp)])
#             player2.setPiece("X" if player1.getPiece() == "O" else "O")
#             lbl_status["text"] = player2.getName() + " se ha conectado!"
#             sleep(3)
#             toggle_turn(player1.getPiece() == "O")

#         elif from_server.startswith("~xy~"):
#             temp = from_server.replace("~xy~", "")
#             _x = temp[0:temp.find("~")]
#             _y = temp[temp.find("~") + 1:len(temp)]


#     sckt.close()

window_main.mainloop()
