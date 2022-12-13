import re
from template import Day

class Solution(Day):

  def __init__(self):
    super().__init__(__file__)

  @staticmethod
  def split_lines(data):
    crate_lines = []
    move_lines = []
    current = "CRATES"
    
    for line in data:
      if line == "\n":
        current = "MOVES"
        crate_lines.pop()
        continue

      if current == "CRATES":
        crate_lines.append(line)
      else:
        move_lines.append(line)

    return (crate_lines, move_lines)

  @staticmethod
  def build_crates(crates):
    # Build Crates
    stacks = []
    step = 4
    crate_regex = re.compile("\[([A-Z])\]")
    for n, line in enumerate(crates):
      stack = 0
      for i in range(0, len(line), step):
        if n == 0:
          stacks.append([])

        crate = line[i:i+step-1]
        if crate.strip() != "":
          stacks[stack].append(crate_regex.sub(r"\1", crate))

        stack += 1

    return stacks

  @staticmethod
  def parse_moves(line):
    m = re.match("move (?P<count>[0-9]+) from (?P<start>[0-9]+) to (?P<end>[0-9]+)", line)
    return m.groups()

  @staticmethod
  def move_crates(stacks, moves, move_function):
    # Iterate moves
    for n, move in enumerate(moves):
      (count, start, end) = Solution.parse_moves(move)

      count = int(count)
      start = int(start)-1
      end = int(end)-1

      crates = stacks[start][0:count]
      stacks[start] = stacks[start][count:]
      stacks[end] = move_function(crates, stacks[end])

    return stacks
    
  def get_crates(self, data):
    (crates, moves) = self.split_lines(data)
    stacks = self.build_crates(crates)
    return (stacks, moves)

  def task_1(self, data):
    (stacks, moves) = self.get_crates(data)
    stacks = self.move_crates(stacks, moves, lambda new, old: list(reversed(new)) + old)

    # Find top cra tes
    tops = []
    for stack in stacks:
      tops.append(stack.pop(0))

    print("The answer to task 1 is: ", ''.join(tops))
  
  def task_2(self, data):
    (stacks, moves) = self.get_crates(data)
    stacks = self.move_crates(stacks, moves, lambda new, old: new + old)
    
    # Find top cra tes
    tops = []
    for stack in stacks:
      tops.append(stack.pop(0))

    print("The answer to task 2 is: ", ''.join(tops))
    