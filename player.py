class Player:
  def __init__(self, name, color, score, piece):
    self.name = name
    self.score = score
    self.color = color
    self.piece = piece
  

  def setName(self, name):
    self.name = name
  def getName(self):
    return self.name
  
  def setScore(self, score):
    self.score = score
  def getScore(self):
    return self.score

  def setColor(self, color):
    self.color = color
  def getColor(self):
    return self.color

  def setPiece(self, piece):
    self.piece = piece
  def getPiece(self):
    return self.piece
  