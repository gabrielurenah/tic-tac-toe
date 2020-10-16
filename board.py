class Board:
  board = []

  def getBoard(self):
    return self.board

  def draw_winning_pattern(self, l, indexes):
    for i in indexes: l[i]["label"].config(foreground="green", highlightbackground="green", highlightcolor="green", highlightthicknes=2)
  
  # [(0,0) -> (0,1) -> (0,2)], [(1,0) -> (1,1) -> (1,2)], [(2,0), (2,1), (2,2)]
  def check_row(self):
    list_symbols, list_labels_temp = [], []
    winner = False
    win_symbol = ""
    b = self.board
    for i in range(len(b)):
        list_symbols.append(b[i]["symbol"])
        list_labels_temp.append(b[i])
        if (i + 1) % 3 == 0:
            if (list_symbols[0] == list_symbols[1] == list_symbols[2]):
                if list_symbols[0] != "":
                    winner = True
                    win_symbol = list_symbols[0]
                    self.draw_winning_pattern(list_labels_temp,[0,1,2])
            list_symbols = []
            list_labels_temp = []

    return [winner, win_symbol]

  # [(0,0) -> (1,0) -> (2,0)], [(0,1) -> (1,1) -> (2,1)], [(0,2), (1,2), (2,2)]
  def check_col(self):
    winner = False
    win_symbol = ""
    b = self.board
    CANT_COL = 3
    
    for i in range(CANT_COL):
        if (b[i]["symbol"] ==
            b[i + CANT_COL]["symbol"] ==
            b[i + CANT_COL + CANT_COL]["symbol"]):
            if b[i]["symbol"] != "":
                winner = True
                win_symbol = b[i]["symbol"]
                self.draw_winning_pattern(b,[i, i+ CANT_COL, i+CANT_COL+CANT_COL])

    return [winner, win_symbol]

  def check_diagonal(self):
    winner = False
    win_symbol = ""
    i, j, CANT_COL = 0, 2 ,3
    b = self.board

    # top-left to bottom-right diagonal (0, 0) -> (1,1) -> (2, 2)
    if b[i]["symbol"] == b[i + (CANT_COL + 1)]["symbol"] == b[(CANT_COL + CANT_COL) + (i + 2)]["symbol"]:
        if b[i]["symbol"] != "":
            winner = True
            win_symbol = b[i]["symbol"]
            self.draw_winning_pattern(b,[i, i + (CANT_COL + 1), (CANT_COL + CANT_COL) + (i + 2)])

    # top-right to bottom-left diagonal (0, 0) -> (1,1) -> (2, 2)
    elif b[j]["symbol"] == b[j + (CANT_COL - 1)]["symbol"] == b[j + (CANT_COL + 1)]["symbol"]:
        if b[j]["symbol"] != "":
            winner = True
            win_symbol = b[j]["symbol"]
            self.draw_winning_pattern(b, [j, j + (CANT_COL - 1), j + (CANT_COL + 1)])
    else:
        winner = False

    return [winner, win_symbol]

  # si todas las celdas estan llenas y no hay ganador, hay un empate
  def check_for_draw(self):
    b = self.board
    for i in range(len(b)):
        if b[i]["ticked"] is False:
            return [False, ""]
    return [True, ""]

  def status(self):
    result = self.check_row()
    if result[0]:
        return result
    result = self.check_col()
    if result[0]:
        return result
    result = self.check_diagonal()
    if result[0]:
        return result
    result = self.check_for_draw()
    return result
   