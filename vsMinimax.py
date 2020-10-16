import numpy as np
from math import inf as infinity
import os

board = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
players = ['X','O']

WIN = 1
DRAW = 0
NA = -1

def play_move(state, player, block_num):
    if state[int((block_num-1)/3)][(block_num-1)%3] == ' ':
        state[int((block_num-1)/3)][(block_num-1)%3] = player
    else:
        block_num = int(input("Posicion ocupada. Elija otro numero: "))
        play_move(state, player, block_num)
    
def copy_board(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state
    
def check_current_state(board):
    # Check if draw
    draw_flag = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                draw_flag = 1
    if draw_flag == 0:
        return None, DRAW
    
    # Check horizontals
    for i in range(3):
      if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != ' '):
          return board[i][0], WIN
    
    # Check verticals
    if (board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != ' '):
        return board[0][0], WIN
    if (board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != ' '):
        return board[0][1], WIN
    if (board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != ' '):
        return board[0][2], WIN
    
    # Check diagonals
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != ' '):
        return board[1][1], WIN
    if (board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != ' '):
        return board[1][1], WIN
    
    return None, NA

def print_board(board):
    print('----------------')
    for i in range(3):
        print('| ' + str(board[i][0]) + ' || ' + str(board[i][1]) + ' || ' + str(board[i][2]) + ' |')
        print('----------------')
    
## Minimax 
def getBestMove(state, player):
    winner, done = check_current_state(state)
    if done == WIN: 
        return 1 if  winner == 'O' else -1
    elif done == DRAW:   
        return 0
        
    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                empty_cells.append(i*3 + (j+1))
    
    for empty_cell in empty_cells:
        move = {}
        move['index'] = empty_cell
        new_state = copy_board(state)
        play_move(new_state, player, empty_cell)
        
        # mas profundidad en el arbol del humano o CPU
        result = getBestMove(new_state, 'X' if player == 'O' else 'O')   
        move['score'] = result
        
        moves.append(move)

    # encontrar mejor mov
    best_move = None
    if player == 'O':   # si es CPU
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']
                
    return best_move

# PLaying
while True:
    board = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
    current_state = NA
    os.system('clear')
    print("\nJuego Nuevo!")
    print_board(board)
    player_choice = input("Quien juega primero? x (Humano) - o(CPU): ")
    winner = None
    
    current_player_idx = 0 if player_choice == 'x' else 1
    
    while current_state == NA:
        if current_player_idx == 0: 
            block_choice = int(input("Elija un numero del (1 to 9): "))
            play_move(board ,players[current_player_idx], block_choice)
        else: 
            block_choice = getBestMove(board, players[current_player_idx])
            play_move(board ,players[current_player_idx], block_choice)
            print("AI plays move: " + str(block_choice))

        os.system('clear')
        print_board(board)
        winner, current_state = check_current_state(board)
        if winner != None:
            print("Ganador: " + str(winner))
        else:
            current_player_idx = (current_player_idx + 1)%2
        
        if current_state == DRAW:
            print("Empate")

    