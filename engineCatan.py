import random
import engine
from engine import gameData

class player:
  def __init__(self, name, rank = None):
    self.rank = rank
    self.name = name
    self.resources = {res: 0 for res in gameData["resources"]}
    self.otherCards = {card: 0 for card in gameData["gamblingCardTypes"]}
    self.vps = 0

  def checkResources(self, needed):
    for resource, amount in needed.items():
      if self.resources.get(resource, 0) < amount:
        return False
    return True

  def buyCard(self, card="gamblingCard"):
    if card not in gameData["prices"]:
      engine.handleError("cardTypeNotFound")
      return KeyError
    
    cardPrice = gameData["prices"][card]
    if self.checkResources(cardPrice):
      choice = random.choice(gameData["gamblingCardTypes"])
      for resource, cost in cardPrice.items():
        self.resources[resource] -= cost
      self.otherCards[choice] += 1
      return choice
    return None

class hexagon():
  def __init__(self, resource, number):
    self.resource = resource
    self.number = number

  def activate(self):
    hexagonActivatedDialogue = engine.dialogue["system"]["events"]["hexagonActivated"]
    engine.logEvent(engine.formatStyled(hexagonActivatedDialogue, replace = [self.resource, self.number]))

class board:
  def __init__(self, grid):
    self.hexagons = []
    self.roads = []
    self.settlements = []

  def printBoard(self):
    pass

class road:
  def __init__(self, owner):
    self.owner = owner

class settlement:
  def __init__(self, owner):
    self.owner = owner
    self.vps = 1
    self.type = "village"
  
  def upgrade(self):
    if self.type == "village":
      self.type = "city"
      self.vps = 2
      return True
    return False

engine.logEvent(engine.dialogue["system"]["events"]["loadedEngine"])