import re
import json
import random

class AntrophioGame(object):
  
  re_search = re.compile(r'[^a-zA-Z0-9_]').search

  def __init__(self):
    self.nextid = 0
    self.players = {}
    self.black, self.white = [], []
    self.black_discarded, self.wite_discarded = [], []
    self.decks = []
    self.playing, self.primed = False, False

  def load_deck(self, name):
    if name in self.decks:
      return
    if bool(re_search(name)):
      raise ValueError("Invalid deck name")
    with open(name) as f:
      deck = json.load(f)
    for card in deck["blackCards"] + deck["whiteCards"]:
      card["watermark"] = deck["watermark"]
    self.black.extend(deck["blackCards"])
    self.white.extend(deck["whiteCards"])
    self.decks.append(name)
    if not deck["expansion"]:
      self.primed = True

  def _black(self):
    if not self.black:
      random.shuffle(self.black_discarded)
      self.black = self.black_discarded
      self.black_discarded = []
    return self.black.pop()

  def _white(self):
    if not self.white:
      random.shuffle(self.white_discarded)
      self.white = self.white_discarded
      self.white_discarded = []
    return self.white.pop()

  def join(self, player):
    playerid = self.nextid
    self.nextid += 1
    player["hand"], player["score"] = [], 0
    self.players[playerid] = player
    return playerid

  def deal(self):
    result = {}
    for id, player in self.players.iteritems():
      while len(player["hand"]) < 10:
        player["hand"].append(self._white())
      result[id] = player["hand"]
    return result

  def round(self):
    if not self.primed:
      raise RuntimeError("No deck, no dice.")
    if self.playing:
      raise RuntimeError("Already playing!")
    self.playing = True
    card = self._black()
    self.table = (card, {})
    return card

  def play(self, playerid, cardid):
    card = self.players[playerid].pop(cardid)
    self.table[1][playerid] = card
    self.white_discarded.append(card)
  
  def czar(self):
    return self.table

  def pick(self, playerid):
    self.players[playerid]["score"] += 1
    self.black_discarded.append(self.table[0])
    self.table = None
    return {playerid: self.players[playerid]["score"] 
              for playerid in self.players}
