class Board:
  board = []

  def getBoard(self):
    return self.board

  def draw_winning_pattern(self, l, indexes):
    for i in indexes: l[i]["label"].config(foreground="green", highlightbackground="green", highlightcolor="green", highlightthicknes=2)
  
  # [(0,0) -> (0,1) -> (0,2)], [(1,0) -> (1,1) -> (1,2)], [(2,0), (2,1), (2,2)]
  def check_row(self):
    list_pieces, list_labels_temp = [], []
    winner = False
    winning_piece = ""
    b = self.board
    for i in range(len(b)):
        list_pieces.append(b[i]["piece"])
        list_labels_temp.append(b[i])
        if (i + 1) % 3 == 0:
            if (list_pieces[0] == list_pieces[1] == list_pieces[2]):
                if list_pieces[0] != "":
                    winner = True
                    winning_piece = list_pieces[0]
                    self.draw_winning_pattern(list_labels_temp,[0,1,2])
            list_pieces = []
            list_labels_temp = []

    return [winner, winning_piece]

  # [(0,0) -> (1,0) -> (2,0)], [(0,1) -> (1,1) -> (2,1)], [(0,2), (1,2), (2,2)]
  def check_col(self):
    winner = False
    winning_piece = ""
    b = self.board
    CANT_COL = 3
    
    for i in range(CANT_COL):
        if (b[i]["piece"] ==
            b[i + CANT_COL]["piece"] ==
            b[i + CANT_COL + CANT_COL]["piece"]):
            if b[i]["piece"] != "":
                winner = True
                winning_piece = b[i]["piece"]
                self.draw_winning_pattern(b,[i, i+ CANT_COL, i+CANT_COL+CANT_COL])

    return [winner, winning_piece]

  def check_diagonal(self):
    winner = False
    winning_piece = ""
    i, j, CANT_COL = 0, 2 ,3
    b = self.board

    # top-left to bottom-right diagonal (0, 0) -> (1,1) -> (2, 2)
    if b[i]["piece"] == b[i + (CANT_COL + 1)]["piece"] == b[(CANT_COL + CANT_COL) + (i + 2)]["piece"]:
        if b[i]["piece"] != "":
            winner = True
            winning_piece = b[i]["piece"]
            self.draw_winning_pattern(b,[i, i + (CANT_COL + 1), (CANT_COL + CANT_COL) + (i + 2)])

    # top-right to bottom-left diagonal (0, 0) -> (1,1) -> (2, 2)
    elif b[j]["piece"] == b[j + (CANT_COL - 1)]["piece"] == b[j + (CANT_COL + 1)]["piece"]:
        if b[j]["piece"] != "":
            winner = True
            winning_piece = b[j]["piece"]
            self.draw_winning_pattern(b, [j, j + (CANT_COL - 1), j + (CANT_COL + 1)])
    else:
        winner = False

    return [winner, winning_piece]

  # si todas las celdas estan llenas y no hay ganador, hay un empate
  def check_for_draw(self):
    b = self.board
    for i in range(len(b)):
        if b[i]["piece"] == "":
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
   