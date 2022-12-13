from template import Day
from time import time

WIN = 6
DRAW = 3

choices =  {
  "A": 1,
  "B": 2,
  "C": 3,
  "X": 1,
  "Y": 2,
  "Z": 3
}

class Solution(Day):

  def __init__(self):
    super().__init__(__file__)

  def prep_data(self, data):
    self.data = data

  def task_1(self):
    start = time()
    moves = {
      "A": "Y",
      "B": "Z",
      "C": "X",
    }

    weapons = {
      "A": "X",
      "B": "Y",
      "C": "Z"
    }

    score = 0
    for game in self.data:
        (opponent, me) = game.strip().split(" ")
        score += choices[me]

        if moves[opponent] == me:
          score += WIN
        elif weapons[opponent] == me:
          score += DRAW

    self.log_answer(1, score, start)

  def task_2(self):
    start = time()
    results = {
      "X": "Lose",
      "Y": "Draw",
      "Z": "Win"
    }

    moves = {
      "A": {
        "X": "C",
        "Y": "A",
        "Z": "B"
      },
      "B": {
        "X": "A",
        "Y": "B",
        "Z": "C"
      },
      "C": {
        "X": "B",
        "Y": "C",
        "Z": "A"
      }
    }

    score = 0

    for game in self.data:
        (opponent, result) = game.strip().split(" ")
        me = moves[opponent][result]
        score += choices[me]

        if results[result] == "Win":
          score += WIN
        elif results[result] == "Draw":
          score += DRAW

    self.log_answer(2, score, start)