import re
from template import Day
from time import time

class Solution(Day):

  moves = []
  move_regex = re.compile("(?P<direction>U|D|L|R) (?P<moves>[0-9]+)")
  
  def __init__(self):
    super().__init__(__file__)

  @staticmethod
  def build_rope(knots):
    rope = []
    positions = []
    for _ in range(knots):
      rope.append([0,0])
      positions.append(set(["0,0"]))

    return (rope, positions)

  @staticmethod
  def parse_move(line):
    m = Solution.move_regex.match(line.strip())
    move = m.groupdict()
    move["moves"] = int(move["moves"])
    return move

  @staticmethod
  def match_knot(index, rope, positions):
    h = rope[index-1]
    t = rope[index]

    if abs(h[0] - t[0]) <= 1 and abs(h[1] - t[1]) <= 1:
      return positions

    # Vertical
    if h[0] == t[0]:
      if h[1] > t[1]+1:
        t[1] += 1
      elif h[1] < t[1]-1:
        t[1] -= 1
    # Horizontal
    elif h[1] == t[1]:
      if h[0] > t[0]+1:
        t[0] += 1
      elif h[0] < t[0]-1:
        t[0] -= 1
    # Diagonal
    else:
      if h[1] > t[1]:
        t[1] += 1
      elif h[1] < t[1]:
        t[1] -= 1
      if h[0] > t[0]:
        t[0] += 1
      elif h[0] < t[0]:
        t[0] -= 1

    position = "%i,%i" % (t[0], t[1])
    positions[index].add(position)

    return positions

  @staticmethod
  def do_move(move, rope, positions):
    if move["direction"] == "U":
      for _ in range(move["moves"]):
        rope[0][1] += 1
        for i in range(1,len(rope)):
          positions = Solution.match_knot(i, rope, positions)
    elif move["direction"] == "D":
      for _ in range(move["moves"]):
        rope[0][1] -= 1
        for i in range(1,len(rope)):
          positions = Solution.match_knot(i, rope, positions)
    elif move["direction"] == "L":
      for _ in range(move["moves"]):
        rope[0][0] -= 1
        for i in range(1,len(rope)):
          positions = Solution.match_knot(i, rope, positions)
    elif move["direction"] == "R":
      for _ in range(move["moves"]):
        rope[0][0] += 1
        for i in range(1,len(rope)):
          positions = Solution.match_knot(i, rope, positions)

    return (rope, positions)

  def swing_rope(self, rope, positions):
    for move in self.moves:
      (rope, positions) = Solution.do_move(move, rope, positions)

    return (rope, positions)

  def prep_data(self, data):
    for line in data:
      self.moves.append(Solution.parse_move(line))

  def task_1(self):
    start = time()
    (_, positions) = self.swing_rope(*self.build_rope(2))
  
    self.log_answer(1, len(set(positions[-1])), start)

  def task_2(self):
    start = time()
    (_, positions) = self.swing_rope(*self.build_rope(10))
  
    self.log_answer(2, len(set(positions[-1])), start)
